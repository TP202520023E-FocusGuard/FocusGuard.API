from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import (
    AuthenticationException,
    BusinessException,
    DatabaseException,
    NotFoundException,
)
from app.modules.users.schemas.user_schema import (
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordResetRequestResponse
)
from ..services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

def get_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    service = UserService(db)
    try:
        return await service.create_user(user_data)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except DatabaseException as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.get("/", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)) -> list[UserResponse]:
    service = UserService(db)
    try:
        return await service.get_all_users()
    except DatabaseException as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    service = UserService(db)
    try:
        return await service.get_user_by_id(user_id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except DatabaseException as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.get("/by-email/{email}", response_model=UserResponse)
async def get_user_by_email(
    email: str, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    service = UserService(db)
    try:
        return await service.get_user_by_email(email)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except DatabaseException as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    service = UserService(db)
    try:
        return await service.update_user(user_id, user_data)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except DatabaseException as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> Response:
    service = UserService(db)
    try:
        await service.delete_user(user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except DatabaseException as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
) -> Token:
    service = UserService(db)
    try:
        return await service.login(credentials)
    except AuthenticationException as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    except DatabaseException as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

@router.post("/password-reset-request", status_code=status.HTTP_200_OK)
async def request_password_reset(
    request: PasswordResetRequest,
    service: UserService = Depends(get_service),
):
    result = await service.request_password_reset(request)
    return result

@router.post("/password-reset-confirm", status_code=status.HTTP_200_OK)
async def confirm_password_reset(
    reset_confirm: PasswordResetConfirm,
    service: UserService = Depends(get_service),
):
    """
    Confirma el restablecimiento de contraseña
    """

    try:
        await service.reset_password(reset_confirm)
        return {"message": "Contraseña restablecida exitosamente"}
    except AuthenticationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))