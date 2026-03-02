from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.content_user_model import ContentUserModel
from ..schemas.content_user_schema import ContentUserCreate, ContentUserUpdate


class ContentUserRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(self, data: ContentUserCreate) -> ContentUserModel:
        registro = ContentUserModel(
            id_usuarios=data.id_usuarios,
            id_sitios_web_usuario=data.id_sitios_web_usuario,
            id_contenidos=data.id_contenidos,
            id_categorias_contenido=data.id_categorias_contenido,
        )

        try:
            self.db.add(registro)
            await self.db.commit()
            await self.db.refresh(registro)
            return registro
        except IntegrityError as exc:
            await self.db.rollback()
            raise ValueError(
                "Ya existe un registro para este usuario, sitio web y contenido"
            ) from exc
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_all(self) -> list[ContentUserModel]:
        registros = await self.db.scalars(select(ContentUserModel))
        return list(registros.all())

    async def get_by_id(self, record_id: int) -> Optional[ContentUserModel]:
        return await self.db.get(ContentUserModel, record_id)

    async def get_by_user(self, user_id: int) -> list[ContentUserModel]:
        stmt = select(ContentUserModel).where(ContentUserModel.id_usuarios == user_id)
        registros = await self.db.scalars(stmt)
        return list(registros.all())

    async def get_by_user_and_site(
        self, user_id: int, site_id: int
    ) -> list[ContentUserModel]:
        stmt = select(ContentUserModel).where(
            ContentUserModel.id_usuarios == user_id,
            ContentUserModel.id_sitios_web_usuario == site_id,
        )
        registros = await self.db.scalars(stmt)
        return list(registros.all())

    # async def get_by_user_site_and_content(
    #     self, user_id: int, site_id: int, content_id: int
    # ) -> list[ContentUserModel]:
    #     stmt = select(ContentUserModel).where(
    #         ContentUserModel.id_usuarios == user_id,
    #         ContentUserModel.id_sitios_web_usuario == site_id,
    #         ContentUserModel.id_contenidos == content_id,
    #     )
    #     registros = await self.db.scalars(stmt)
    #     return list(registros.all())

    async def get_by_user_site_and_content(
        self, user_id: int, site_id: int, content_id: int
    ) -> Optional[ContentUserModel]:
        stmt = select(ContentUserModel).where(
            ContentUserModel.id_usuarios == user_id,
            ContentUserModel.id_sitios_web_usuario == site_id,
            ContentUserModel.id_contenidos == content_id,
        )
        return (await self.db.scalars(stmt)).one_or_none()

    async def get_by_user_and_category(
        self, user_id: int, category_id: int
    ) -> list[ContentUserModel]:
        stmt = select(ContentUserModel).where(
            ContentUserModel.id_usuarios == user_id,
            ContentUserModel.id_categorias_contenido == category_id,
        )
        registros = await self.db.scalars(stmt)
        return list(registros.all())

    async def update_by_id(
            self,
            content_user_id: int,
            data: ContentUserUpdate,
    ) -> ContentUserModel:
        registro = await self.get_by_id(content_user_id)

        if registro is None:
            raise ValueError("No se encontró el registro solicitado.")

        if data.id_categorias_contenido is not None:
            registro.id_categorias_contenido = data.id_categorias_contenido

        try:
            self.db.add(registro)
            await self.db.commit()
            await self.db.refresh(registro)
        except SQLAlchemyError:
            await self.db.rollback()
            raise

        return registro

    async def delete(self, registro: ContentUserModel) -> None:
        try:
            await self.db.delete(registro)
            await self.db.commit()
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def delete_by_id(self, record_id: int) -> bool:
        registro = await self.get_by_id(record_id)

        if registro is None:
            return False

        await self.delete(registro)
        return True