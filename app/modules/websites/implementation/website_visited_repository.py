from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.website_visited_model import WebsiteVisitedModel
from ..schemas.website_visited_schema import WebsiteVisitedCreate


class WebsiteVisitedRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(self, data: WebsiteVisitedCreate) -> WebsiteVisitedModel:
        registro = WebsiteVisitedModel(
            id_usuarios=data.id_usuarios,
            id_sitios_web_usuario=data.id_sitios_web_usuario,
            fecha_hora_ingreso=data.fecha_hora_ingreso,
            fecha_hora_salida=data.fecha_hora_salida,
            id_categorias_web_snapshot=data.id_categorias_web_snapshot,
        )

        try:
            self.db.add(registro)
            await self.db.commit()
            await self.db.refresh(registro)
            return registro
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_by_id(self, visit_id: int) -> Optional[WebsiteVisitedModel]:
        return await self.db.get(WebsiteVisitedModel, visit_id)

    async def get_by_user(self, user_id: int) -> list[WebsiteVisitedModel]:
        stmt = (
            select(WebsiteVisitedModel)
            .where(WebsiteVisitedModel.id_usuarios == user_id)
            .order_by(WebsiteVisitedModel.fecha_hora_ingreso.desc())
        )

        registros = (await self.db.scalars(stmt)).all()
        return list(registros)

    async def get_by_user_and_interval(
        self,
        user_id: int,
        start: datetime,
        end: datetime,
    ) -> list[WebsiteVisitedModel]:
        stmt = (
            select(WebsiteVisitedModel)
            .where(
                WebsiteVisitedModel.id_usuarios == user_id,
                WebsiteVisitedModel.fecha_hora_ingreso >= start,
                WebsiteVisitedModel.fecha_hora_salida.is_not(None),
                WebsiteVisitedModel.fecha_hora_salida <= end,
            )
            .order_by(WebsiteVisitedModel.fecha_hora_ingreso.desc())
        )

        registros = (await self.db.scalars(stmt)).all()
        return list(registros)

    async def update_exit_time(
            self,
            registro: WebsiteVisitedModel,
            fecha_hora_salida: datetime,
    ) -> WebsiteVisitedModel:
        registro.fecha_hora_salida = fecha_hora_salida

        try:
            await self.db.commit()
            await self.db.refresh(registro)
            return registro
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def delete_by_id(self, visit_id: int) -> bool:
        registro = await self.get_by_id(visit_id)

        if registro is None:
            return False

        try:
            await self.db.delete(registro)
            await self.db.commit()
            return True
        except SQLAlchemyError:
            await self.db.rollback()
            raise