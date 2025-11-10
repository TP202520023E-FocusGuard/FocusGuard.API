from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from app.modules.categories.models.category_model import ChangeCategoryModel
from app.modules.categories.schemas.category_schema import ChangeCategoryCreate

class CategoryRepository:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session
    
    async def get_all(self) -> List[ChangeCategoryModel]:
        stmt = select(ChangeCategoryModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, change_id: int) -> Optional[ChangeCategoryModel]:
        stmt = select(ChangeCategoryModel).where(ChangeCategoryModel.id == change_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(self, data: ChangeCategoryCreate) -> ChangeCategoryModel:
        nuevo_cambio = ChangeCategoryModel(**data)
        self.session.add(nuevo_cambio)
        await self.session.commit()
        await self.session.refresh(nuevo_cambio)
        return nuevo_cambio
    