from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import label
from sqlalchemy import func

from app.modules.categories.models.category_website_model import CategoryWebsiteModel
from app.modules.websites.models.website_model import WebsiteModel
from app.modules.websites.models.website_user_model import WebsiteUserModel
from ..models.website_visited_model import WebsiteVisitedModel
from ..schemas.website_visited_schema import WebsiteVisitedCreate


class WebsiteVisitedRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(self, data: WebsiteVisitedCreate) -> WebsiteVisitedModel:
        registro = WebsiteVisitedModel(
            id_usuarios=data.id_usuarios,
            id_sitios_web_usuario=data.id_sitios_web_usuario,
            id_categorias_web=data.id_categorias_web,
            fecha_hora_ingreso=data.fecha_hora_ingreso,
            fecha_hora_salida=data.fecha_hora_salida
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
    
    async def get_summary_by_user_and_interval(
        self,
        user_id: int,
        start: datetime | None,
        end: datetime | None,
    ):
        filters = [
            WebsiteVisitedModel.id_usuarios == user_id,
            WebsiteVisitedModel.fecha_hora_salida.isnot(None),
        ]

        if start is not None:
            filters.append(WebsiteVisitedModel.fecha_hora_ingreso >= start)

        if end is not None:
            filters.append(WebsiteVisitedModel.fecha_hora_ingreso <= end)

        stmt = (
            select(
                WebsiteModel.dominio.label("domain"),
                WebsiteVisitedModel.id_sitios_web_usuario.label("site_user_id"),

                func.count(WebsiteVisitedModel.id).label("total_visits"),

                (func.sum(
                    func.timestampdiff(
                        text("SECOND"),
                        WebsiteVisitedModel.fecha_hora_ingreso,
                        WebsiteVisitedModel.fecha_hora_salida
                    )
                ) / 60).label("total_minutes"),

                func.min(WebsiteVisitedModel.fecha_hora_ingreso).label("first_visit"),
                func.max(WebsiteVisitedModel.fecha_hora_ingreso).label("last_visit"),

                CategoryWebsiteModel.codigo.label("category"),
            )
            .select_from(WebsiteVisitedModel)
            .join(
                WebsiteUserModel,
                WebsiteUserModel.id == WebsiteVisitedModel.id_sitios_web_usuario
            )
            .join(
                WebsiteModel,
                WebsiteModel.id == WebsiteUserModel.id_sitios_web
            )
            .join(
                CategoryWebsiteModel,
                CategoryWebsiteModel.id == WebsiteVisitedModel.id_categorias_web
            )
            .where(*filters)
            .group_by(
                WebsiteModel.dominio,
                CategoryWebsiteModel.codigo,
                WebsiteVisitedModel.id_sitios_web_usuario
            )
            .order_by(func.sum(
                func.timestampdiff(
                    text("SECOND"),
                    WebsiteVisitedModel.fecha_hora_ingreso,
                    WebsiteVisitedModel.fecha_hora_salida
                )
            ).desc())
        )

        result = await self.db.execute(stmt)
        return result.mappings().all()