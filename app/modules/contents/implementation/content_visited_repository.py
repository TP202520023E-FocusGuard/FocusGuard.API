from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.content_visited_model import ContentVisitedModel
from ..schemas.content_visited_schema import ContentVisitedCreate


class ContentVisitedRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(self, data: ContentVisitedCreate) -> ContentVisitedModel:
        registro = ContentVisitedModel(
            id_usuarios=data.id_usuarios,
            id_contenidos_usuario=data.id_contenidos_usuario,
            fecha_hora_ingreso=data.fecha_hora_ingreso,
            fecha_hora_salida=data.fecha_hora_salida,
        )

        try:
            self.db.add(registro)
            await self.db.commit()
            await self.db.refresh(registro)
            return registro
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_all(self) -> list[ContentVisitedModel]:
        stmt = select(ContentVisitedModel).order_by(
            ContentVisitedModel.fecha_hora_ingreso.desc()
        )
        registros = (await self.db.scalars(stmt)).all()
        return list(registros)

    async def get_by_id(self, record_id: int) -> Optional[ContentVisitedModel]:
        return await self.db.get(ContentVisitedModel, record_id)

    async def get_by_user(self, user_id: int) -> list[ContentVisitedModel]:
        stmt = (
            select(ContentVisitedModel)
            .where(ContentVisitedModel.id_usuarios == user_id)
            .order_by(ContentVisitedModel.fecha_hora_ingreso.desc())
        )
        registros = (await self.db.scalars(stmt)).all()
        return list(registros)

    async def get_by_user_and_content_user(
        self, user_id: int, content_user_id: int
    ) -> list[ContentVisitedModel]:
        stmt = (
            select(ContentVisitedModel)
            .where(
                ContentVisitedModel.id_usuarios == user_id,
                ContentVisitedModel.id_contenidos_usuario == content_user_id,
            )
            .order_by(ContentVisitedModel.fecha_hora_ingreso.desc())
        )
        registros = (await self.db.scalars(stmt)).all()
        return list(registros)

    async def delete_by_id(self, record_id: int) -> bool:
        registro = await self.get_by_id(record_id)

        if registro is None:
            return False

        try:
            await self.db.delete(registro)
            await self.db.commit()
            return True
        except SQLAlchemyError:
            await self.db.rollback()
            raise