from ..implementation.category_website_repository import CategoryWebsiteRepository
from ..schemas.category_website_schema import (
    CategoryWebsiteCreate,
    CategoryWebsiteResponse,
)


class CategoryWebsiteService:
    def __init__(self, repo: CategoryWebsiteRepository):
        self.repo = repo

    async def create_category_website(self, data: CategoryWebsiteCreate) -> CategoryWebsiteResponse:
        categoria = await self.repo.create(data)
        return CategoryWebsiteResponse.model_validate(categoria)

    async def get_all(self) -> list[CategoryWebsiteResponse]:
        categorias = await self.repo.get_all()
        return [CategoryWebsiteResponse.model_validate(cat) for cat in categorias]

    async def get_by_id(self, category_id: int) -> CategoryWebsiteResponse:
        categoria = await self.repo.get_by_id(category_id)
        if categoria is None:
            raise ValueError("Categoría web no encontrada")
        return CategoryWebsiteResponse.model_validate(categoria)

    async def get_by_name(self, nombre: str) -> CategoryWebsiteResponse:
        categoria = await self.repo.get_by_name(nombre)
        if categoria is None:
            raise ValueError("Categoría web no encontrada")
        return CategoryWebsiteResponse.model_validate(categoria)

    async def get_by_code(self, codigo: str) -> CategoryWebsiteResponse:
        categoria = await self.repo.get_by_code(codigo)
        if categoria is None:
            raise ValueError("Categoría web no encontrada")
        return CategoryWebsiteResponse.model_validate(categoria)

    async def get_by_weight(self, peso: int) -> CategoryWebsiteResponse:
        categoria = await self.repo.get_by_weight(peso)
        if categoria is None:
            raise ValueError("Categoría web no encontrada")
        return CategoryWebsiteResponse.model_validate(categoria)

    async def delete_by_id(self, category_id: int) -> None:
        eliminado = await self.repo.delete_by_id(category_id)
        if not eliminado:
            raise ValueError("Categoría web no encontrada")