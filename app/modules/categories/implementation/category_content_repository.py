from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.category_content_model import CategoryContentModel
from ..schemas.category_content_schema import CategoryContentCreate


class CategoryContentRepository:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def create(self, data: CategoryContentCreate) -> CategoryContentModel:
        nueva_categoria = CategoryContentModel(
            nombre=data.nombre,
            es_ocio=data.es_ocio,
            peso=data.peso,
        )

        try:
            self.db.add(nueva_categoria)
            await self.db.commit()
            await self.db.refresh(nueva_categoria)
            return nueva_categoria
        except Exception:
            await self.db.rollback()
            raise

    async def get_all(self) -> list[CategoryContentModel]:
        result = await self.db.execute(select(CategoryContentModel))
        return list(result.scalars().all())

    async def get_by_id(self, category_id: int) -> Optional[CategoryContentModel]:
        result = await self.db.execute(
            select(CategoryContentModel).where(CategoryContentModel.id == category_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, nombre: str) -> Optional[CategoryContentModel]:
        result = await self.db.execute(
            select(CategoryContentModel).where(CategoryContentModel.nombre == nombre)
        )
        return result.scalar_one_or_none()

    async def get_by_weight(self, peso: int) -> Optional[CategoryContentModel]:
        result = await self.db.execute(
            select(CategoryContentModel).where(CategoryContentModel.peso == peso)
        )
        return result.scalar_one_or_none()

    async def delete_by_id(self, category_id: int) -> bool:
        categoria = await self.get_by_id(category_id)
        if categoria is None:
            return False

        await self.db.delete(categoria)
        await self.db.commit()
        return True