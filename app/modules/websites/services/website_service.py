from typing import Optional
from ..schemas.website_schema import (WebsiteCreate, WebsiteResponse)
from ..implementation.website_repository import WebsiteRepository


class WebsiteService:

    def __init__(self, repo: WebsiteRepository):
        self.repo = repo

    async def crear_website(self, website_data: WebsiteCreate) -> WebsiteResponse:

        # 0. Se agrega la lógica del negocio

        # 1. Llama a la capa de implementación para guardar
        modelo_bd = await self.repo.create(website_data)

        # 2. Transforma el Modelo de BD al DTO de Respuesta
        return WebsiteResponse.model_validate(modelo_bd)