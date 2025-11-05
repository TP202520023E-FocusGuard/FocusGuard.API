from __future__ import annotations

from datetime import datetime

from ..implementation.website_visited_repository import WebsiteVisitedRepository
from ..schemas.website_visited_schema import (WebsiteVisitedCreate, WebsiteVisitedResponse)


class WebsiteVisitedService:
    def __init__(self, repo: WebsiteVisitedRepository) -> None:
        self.repo = repo

    async def create(self, data: WebsiteVisitedCreate) -> WebsiteVisitedResponse:
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