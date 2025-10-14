from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from app.modules.categories.models.category_model import CategoryBaseModel, CategoryUserModel
from app.modules.categories.schemas.category_schema import CategoriaUsuarioCreate

class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all_categories(self) -> List[CategoryBaseModel]:
        """Obtiene todas las categorías base (globales para todos los usuarios)"""
        result = await self.session.execute(select(CategoryBaseModel))
        return result.scalars().all()
    
    async def get_user_categories(self, user_id: int) -> List[CategoryUserModel]:
        """Obtiene las selecciones específicas del usuario"""
        result = await self.session.execute(
            select(CategoryUserModel)
            .where(CategoryUserModel.id_usuario == user_id)
        )
        return result.scalars().all()
    
    async def save_user_categories(
        self, 
        user_id: int, 
        categories: List[CategoriaUsuarioCreate]
    ) -> List[CategoryUserModel]:
        """Guarda/actualiza solo las selecciones del usuario (qué categorías marca como procrastinación)"""
        
        # Para cada categoría a guardar
        for cat in categories:
            # Verificar si ya existe una entrada para este usuario-categoría
            existing = await self.session.execute(
                select(CategoryUserModel)
                .where(
                    and_(
                        CategoryUserModel.id_usuario == user_id,
                        CategoryUserModel.id_categoria == cat.id_categoria
                    )
                )
            )
            existing_record = existing.scalar_one_or_none()
            
            if existing_record:
                # Actualizar registro existente
                existing_record.es_procrastinacion = cat.es_procrastinacion
            else:
                # Crear nuevo registro solo si es True (optimización)
                if cat.es_procrastinacion:
                    new_record = CategoryUserModel(
                        id_usuario=user_id,
                        id_categoria=cat.id_categoria,
                        es_procrastinacion=cat.es_procrastinacion
                    )
                    self.session.add(new_record)
        
        await self.session.commit()
        
        # Devolver las categorías actualizadas del usuario
        return await self.get_user_categories(user_id)
    
    async def get_category_by_id(self, category_id: int) -> Optional[CategoryBaseModel]:
        """Obtiene una categoría base por ID"""
        result = await self.session.execute(
            select(CategoryBaseModel)
            .where(CategoryBaseModel.id_categoria == category_id)
        )
        return result.scalar_one_or_none()