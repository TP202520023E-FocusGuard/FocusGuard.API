from __future__ import annotations
from app.core.exceptions import NotFoundException
from datetime import datetime, timezone

from app.modules.users.implementation.user_repository import UserRepository
from ..implementation.website_user_repository import WebsiteUserRepository
from ..implementation.website_visited_repository import WebsiteVisitedRepository

from ..schemas.website_visited_schema import (WebsiteVisitedCreate, WebsiteVisitedUpdate, WebsiteVisitedResponse)


class WebsiteVisitedService:
    def __init__(
            self,
            repo: WebsiteVisitedRepository,
            user_repo: UserRepository,
            website_user_repo: WebsiteUserRepository
    ) -> None:
        self.repo = repo
        self.user_repo = user_repo
        self.website_user_repo = website_user_repo

    async def create(self, data: WebsiteVisitedCreate) -> WebsiteVisitedResponse:
        user = await self.user_repo.get_by_id(data.id_usuarios)
        if user is None:
            raise NotFoundException("El ID de usuario proporcionado no existe.")

        website_user = await self.website_user_repo.get_by_id(data.id_sitios_web_usuario)
        if website_user is None:
            raise NotFoundException("El ID de sitiosweb_usuario proporcionado no existe.")

        registro = await self.repo.create(data)
        return WebsiteVisitedResponse.model_validate(registro)

    async def get_by_id(self, visit_id: int) -> WebsiteVisitedResponse:
        registro = await self.repo.get_by_id(visit_id)

        if registro is None:
            raise ValueError("No se encontró el registro solicitado.")

        return WebsiteVisitedResponse.model_validate(registro)

    async def get_by_user(self, user_id: int) -> list[WebsiteVisitedResponse]:
        registros = await self.repo.get_by_user(user_id)
        return [WebsiteVisitedResponse.model_validate(item) for item in registros]

    async def get_by_user_and_interval(
        self,
        user_id: int,
        start: datetime,
        end: datetime,
    ) -> list[WebsiteVisitedResponse]:
        if start > end:
            raise ValueError("La fecha inicial no puede ser mayor que la fecha final.")

        registros = await self.repo.get_by_user_and_interval(user_id, start, end)
        return [WebsiteVisitedResponse.model_validate(item) for item in registros]

    async def update_exit_time(
        self,
        visit_id: int,
        data: WebsiteVisitedUpdate
    ) -> WebsiteVisitedResponse:
        registro = await self.repo.get_by_id(visit_id)

        if registro is None:
            raise NotFoundException("No se encontró el registro solicitado.")

        fecha_ingreso_naive = registro.fecha_hora_ingreso

        # 1. Verificar si es naive y forzar a UTC (timezone.utc)
        if fecha_ingreso_naive.tzinfo is None:
            fecha_ingreso_aware = fecha_ingreso_naive.replace(tzinfo=timezone.utc)
        else:
            fecha_ingreso_aware = fecha_ingreso_naive

        if data.fecha_hora_salida < fecha_ingreso_aware:
            raise ValueError(
                "La fecha de salida no puede ser anterior a la fecha de ingreso."
            )

        actualizado = await self.repo.update_exit_time(
            registro, data.fecha_hora_salida
        )
        return WebsiteVisitedResponse.model_validate(actualizado)

    async def delete_by_id(self, visit_id: int) -> None:
        eliminado = await self.repo.delete_by_id(visit_id)

        if not eliminado:
            raise ValueError("No se encontró el registro solicitado.")