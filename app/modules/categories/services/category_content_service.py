from ..implementation.category_content_repository import CategoryContentRepository
from ..schemas.category_content_schema import CategoryContentCreate, CategoryContentResponse


class CategoryContentService:
    def __init__(self, repo: CategoryContentRepository):
        self.repo = repo

    async def create_category_content(
        self, data: CategoryContentCreate
    ) -> CategoryContentResponse:
        categoria = await self.repo.create(data)
        return CategoryContentResponse.model_validate(categoria)

    async def get_all(self) -> list[CategoryContentResponse]:
        categorias = await self.repo.get_all()
        return [CategoryContentResponse.model_validate(cat) for cat in categorias]

    async def get_by_id(self, category_id: int) -> CategoryContentResponse:
        categoria = await self.repo.get_by_id(category_id)
        if categoria is None:
            raise ValueError("Categoría de contenido no encontrada")
        return CategoryContentResponse.model_validate(categoria)

    async def get_by_name(self, nombre: str) -> CategoryContentResponse:
        categoria = await self.repo.get_by_name(nombre)
        if categoria is None:
            raise ValueError("Categoría de contenido no encontrada")
        return CategoryContentResponse.model_validate(categoria)

    async def get_by_weight(self, peso: int) -> CategoryContentResponse:
        categoria = await self.repo.get_by_weight(peso)
        if categoria is None:
            raise ValueError("Categoría de contenido no encontrada")
        return CategoryContentResponse.model_validate(categoria)

    async def delete_by_id(self, category_id: int) -> None:
        eliminado = await self.repo.delete_by_id(category_id)
        if not eliminado:
            raise ValueError("Categoría de contenido no encontrada")