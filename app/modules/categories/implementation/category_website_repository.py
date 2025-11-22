from typing import Optional


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.category_website_model import CategoryWebsiteModel
from ..schemas.category_website_schema import CategoryWebsiteCreate


class CategoryWebsiteRepository:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def create(self, data: CategoryWebsiteCreate) -> CategoryWebsiteModel:
        nueva_categoria = CategoryWebsiteModel(
            nombre=data.nombre,
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

    async def get_all(self) -> list[CategoryWebsiteModel]:
        result = await self.db.execute(select(CategoryWebsiteModel))
        return list(result.scalars().all())

    async def get_by_id(self, category_id: int) -> Optional[CategoryWebsiteModel]:
        result = await self.db.execute(
            select(CategoryWebsiteModel).where(CategoryWebsiteModel.id == category_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, nombre: str) -> Optional[CategoryWebsiteModel]:
        result = await self.db.execute(
            select(CategoryWebsiteModel).where(CategoryWebsiteModel.nombre == nombre)
        )
        return result.scalar_one_or_none()

    async def get_by_weight(self, peso: int) -> Optional[CategoryWebsiteModel]:
        result = await self.db.execute(
            select(CategoryWebsiteModel).where(CategoryWebsiteModel.peso == peso)
        )
        return result.scalar_one_or_none()

    async def delete_by_id(self, category_id: int) -> bool:
        categoria = await self.get_by_id(category_id)
        if categoria is None:
            return False

        await self.db.delete(categoria)
        await self.db.commit()
        return True