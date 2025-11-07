from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DatabaseException, NotFoundException
from app.modules.users.models.user_model import UserModel


class UserRepository:

    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def create(self, user: UserModel) -> UserModel:
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError as exc:
            await self.session.rollback()
            raise DatabaseException(f"Integrity error creating user: {exc}") from exc
        except Exception as exc:  # pragma: no cover - unexpected errors
            await self.session.rollback()
            raise DatabaseException(f"Unexpected error creating user: {exc}") from exc

    async def get_all(self) -> list[UserModel]:
        try:
            result = await self.session.execute(select(UserModel))
            return list(result.scalars().all())
        except Exception as exc:  # pragma: no cover
            raise DatabaseException(f"Error fetching users: {exc}") from exc

    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        try:
            result = await self.session.execute(
                select(UserModel).where(UserModel.id == user_id)
            )
            return result.scalar_one_or_none()
        except Exception as exc:  # pragma: no cover
            raise DatabaseException(f"Error fetching user by id: {exc}") from exc

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        try:
            result = await self.session.execute(
                select(UserModel).where(UserModel.correo == email)
            )
            return result.scalar_one_or_none()
        except Exception as exc:  # pragma: no cover
            raise DatabaseException(f"Error fetching user by email: {exc}") from exc

    async def update(self, user: UserModel) -> UserModel:
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError as exc:
            await self.session.rollback()
            raise DatabaseException(f"Integrity error updating user: {exc}") from exc
        except Exception as exc:  # pragma: no cover
            await self.session.rollback()
            raise DatabaseException(f"Unexpected error updating user: {exc}") from exc

    async def delete(self, user_id: int) -> None:
        try:
            result = await self.session.execute(
                delete(UserModel).where(UserModel.id == user_id)
            )
            if result.rowcount == 0:
                raise NotFoundException(f"User with id {user_id} not found")
            await self.session.commit()
        except NotFoundException:
            raise
        except Exception as exc:  # pragma: no cover
            await self.session.rollback()
            raise DatabaseException(f"Error deleting user: {exc}") from exc