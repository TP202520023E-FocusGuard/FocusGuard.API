from ..implementation.content_repository import ContentRepository
from ..schemas.content_schema import ContentCreate, ContentResponse


class ContentService:
    def __init__(self, repo: ContentRepository) -> None:
        self.repo = repo

    async def create_content(self, content_data: ContentCreate) -> ContentResponse:
        registro = await self.repo.create(content_data)
        return ContentResponse.model_validate(registro)

    async def get_contents(self) -> list[ContentResponse]:
        registros = await self.repo.get_all()
        return [ContentResponse.model_validate(item) for item in registros]

    async def get_by_id(self, content_id: int) -> ContentResponse:
        registro = await self.repo.get_by_id(content_id)

        if registro is None:
            raise ValueError("No se encontró un contenido con el id especificado.")

        return ContentResponse.model_validate(registro)

    async def delete_by_id(self, content_id: int) -> None:
        eliminado = await self.repo.delete_by_id(content_id)

        if not eliminado:
            raise ValueError("No se encontró un contenido con el id especificado.")