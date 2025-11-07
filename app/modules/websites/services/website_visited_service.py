from __future__ import annotations
from app.core.exceptions import NotFoundException
from datetime import datetime

from app.modules.users.implementation.user_repository import UserRepository
from ..implementation.website_user_repository import WebsiteUserRepository
from ..implementation.website_visited_repository import WebsiteVisitedRepository

from ..schemas.website_visited_schema import (WebsiteVisitedCreate, WebsiteVisitedResponse)


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

    async def delete_by_id(self, visit_id: int) -> None:
        eliminado = await self.repo.delete_by_id(visit_id)

        if not eliminado:
            raise ValueError("No se encontró el registro solicitado.")