from ..schemas.website_schema import WebsiteCreate, WebsiteResponse
from ..implementation.website_repository import WebsiteRepository


class WebsiteService:

    def __init__(self, repo: WebsiteRepository) -> None:
        self.repo = repo

    async def create_website(self, website_data: WebsiteCreate) -> WebsiteResponse:
        existed_website = await self.repo.get_by_domain(website_data.dominio)

        if existed_website is not None:
            return WebsiteResponse.model_validate(existed_website)

        modelo_bd = await self.repo.create(website_data)
        return WebsiteResponse.model_validate(modelo_bd)

    async def get_websites(self) -> list[WebsiteResponse]:
        registros = await self.repo.get_all()
        return [WebsiteResponse.model_validate(item) for item in registros]

    async def get_by_id(self, website_id: int) -> WebsiteResponse:
        registro = await self.repo.get_by_id(website_id)

        if registro is None:
            raise ValueError("No se encontró un sitio web con el id especificado.")

        return WebsiteResponse.model_validate(registro)

    async def get_by_domain(self, dominio: str) -> WebsiteResponse:
        registro = await self.repo.get_by_domain(dominio)

        if registro is None:
            raise ValueError("No se encontró un sitio web con el dominio especificado.")

        return WebsiteResponse.model_validate(registro)

    async def delete_by_id(self, website_id: int) -> None:
        eliminado = await self.repo.delete_by_id(website_id)

        if not eliminado:
            raise ValueError("No se encontró un sitio web con el id especificado.")

    async def delete_by_domain(self, dominio: str) -> None:
        eliminado = await self.repo.delete_by_domain(dominio)

        if not eliminado:
            raise ValueError("No se encontró un sitio web con el dominio especificado.")