from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.categories.schemas.category_schema import CategoriaBase, CategoriaUsuarioCreate, CategoriaConSeleccion
from app.modules.categories.implementation.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, session: AsyncSession):
        self.repository = CategoryRepository(session)
    
    async def get_all_categories(self) -> List[CategoriaBase]:
        """Returns all base categories from database"""
        categories = await self.repository.get_all_categories()
        return [CategoriaBase.model_validate(cat) for cat in categories]
    
    async def get_categories_with_selection(self, user_id: int) -> List[CategoriaConSeleccion]:
        """Returns categories with user selection from database"""
        base_categories = await self.repository.get_all_categories()
        user_categories = await self.repository.get_user_categories(user_id)
        
        # Crear mapa de selecciones del usuario
        user_selection_map = {uc.id_categoria: uc.es_procrastinacion for uc in user_categories}
        
        return [
            CategoriaConSeleccion(
                id_categoria=cat.id_categoria,
                nombre=cat.nombre,
                descripcion=cat.descripcion,
                es_procrastinacion=user_selection_map.get(cat.id_categoria, False)
            ) for cat in base_categories
        ]
    
    async def save_user_selection(
        self, 
        user_id: int, 
        categories: List[CategoriaUsuarioCreate]
    ) -> List[CategoriaConSeleccion]:
        """Saves user category selection to database"""
        await self.repository.save_user_categories(user_id, categories)
        return await self.get_categories_with_selection(user_id)