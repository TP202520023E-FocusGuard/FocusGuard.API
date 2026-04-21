from datetime import datetime, timedelta, UTC
from sqlalchemy import func
import secrets
from typing import Dict

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import (
    AuthenticationException,
    BusinessException,
    NotFoundException,
)
from app.modules.users.implementation.user_repository import UserRepository
from app.modules.users.models.user_model import UserModel
from app.modules.users.schemas.user_schema import (
    Token,
    TokenPayload,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    PasswordResetRequest,
    PasswordResetConfirm
)

ACCESS_TOKEN_EXPIRE_MINUTES = 5
ALGORITHM = "HS256"

# 🟢 MEMORIA GLOBAL (IMPORTANTE)
RESET_TOKENS: Dict[str, dict] = {}


class UserService:

    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def __init__(self, db_session: AsyncSession):
        self.repository = UserRepository(db_session)

    # -------------------------
    # USERS
    # -------------------------

    async def create_user(self, user_create: UserCreate) -> UserResponse:
        existing_user = await self.repository.get_by_email(user_create.correo)
        if existing_user:
            raise BusinessException("A user with this email already exists")

        user = UserModel(
            correo=user_create.correo,
            contrasenia_hash=self._hash_password(user_create.password),
            nombres=user_create.nombres,
            apellidos=user_create.apellidos,
            telefono=user_create.telefono,
            fecha_registro=func.now(),
            frase_seguridad_hash=self._hash_password(user_create.frase_seguridad)
        )

        created_user = await self.repository.create(user)
        return UserResponse.model_validate(created_user)

    async def get_all_users(self) -> list[UserResponse]:
        users = await self.repository.get_all()
        return [UserResponse.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found")
        return UserResponse.model_validate(user)

    async def get_user_by_email(self, email: str) -> UserResponse:
        user = await self.repository.get_by_email(email)
        if not user:
            raise NotFoundException(f"User with email {email} not found")
        return UserResponse.model_validate(user)

    async def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found")

        update_data = user_update.model_dump(exclude_unset=True)

        password = update_data.pop("password", None)
        if password:
            user.contrasenia_hash = self._hash_password(password)

        for field, value in update_data.items():
            if value is not None:
                setattr(user, field, value)

        updated_user = await self.repository.update(user)
        return UserResponse.model_validate(updated_user)

    async def delete_user(self, user_id: int) -> None:
        await self.repository.delete(user_id)

    # -------------------------
    # AUTH
    # -------------------------

    async def authenticate_user(self, email: str, password: str) -> UserModel:
        user = await self.repository.get_by_email(email)
        if not user or not self._verify_password(password, user.contrasenia_hash):
            raise AuthenticationException("Invalid email or password")
        return user

    async def login(self, credentials: UserLogin) -> Token:
        user = await self.authenticate_user(credentials.correo, credentials.password)

        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        token = self.create_access_token(
            subject=str(user.id),
            email=user.correo,
            expires_delta=expires,
        )

        return Token(
            access_token=token,
            expires_in=int(expires.total_seconds()),
        )

    def create_access_token(self, *, subject: str, email: str, expires_delta: timedelta) -> str:
        expire = datetime.now(UTC) + expires_delta

        payload = {
            "sub": subject,
            "correo": email,
            "exp": int(expire.timestamp()),
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            return TokenPayload(**payload)
        except JWTError:
            raise AuthenticationException("Invalid token")

    # -------------------------
    # PASSWORD RESET (2 PASOS)
    # -------------------------

    async def request_password_reset(self, reset_request: PasswordResetRequest):
        """
        Paso 1: validar usuario + frase de seguridad
        y generar token temporal
        """

        user = await self.repository.get_by_email(reset_request.correo)

        if not user:
            await self._security_delay()
            return {
                "message": "invalid"
            }

        if not self._verify_password(
            reset_request.frase_seguridad,
            user.frase_seguridad_hash
        ):
            await self._security_delay()
            return {
                "message": "invalid"
            }

        # generar token único
        token = secrets.token_urlsafe(32)

        RESET_TOKENS[token] = {
            "email": user.correo,
            "expires": datetime.now(UTC) + timedelta(minutes=10)
        }

        return {
            "message": "valid",
            "token": token
        }

    async def reset_password(self, reset_confirm: PasswordResetConfirm) -> None:
        """
        Paso 2: validar token y cambiar contraseña
        """

        data = RESET_TOKENS.get(reset_confirm.token)

        if not data:
            raise AuthenticationException("Token inválido")

        if data["expires"] < datetime.now(UTC):
            del self._reset_tokens[reset_confirm.token]
            raise AuthenticationException("Token expirado")

        user = await self.repository.get_by_email(data["email"])

        if not user:
            raise NotFoundException("Usuario no encontrado")

        user.contrasenia_hash = self._hash_password(reset_confirm.new_password)
        await self.repository.update(user)

        del RESET_TOKENS[reset_confirm.token]


    def _hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password.encode("utf-8"))

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password.encode("utf-8"), hashed_password)

    async def _security_delay(self):
        import asyncio
        await asyncio.sleep(1.5)