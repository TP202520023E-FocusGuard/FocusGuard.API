from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.modules.goals.models.goal_model import GoalModel

class GoalRepository:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session
    
    async def get_all(self) -> List[GoalModel]:
        stmt = select(GoalModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, goal_id: int) -> Optional[GoalModel]:
        stmt = select(GoalModel).where(GoalModel.id == goal_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: int) -> List[GoalModel]:
        stmt = select(GoalModel).where(GoalModel.id_usuarios == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, data: dict) -> GoalModel:
        nueva_meta = GoalModel(**data)
        self.session.add(nueva_meta)
        await self.session.commit()
        await self.session.refresh(nueva_meta)
        return nueva_meta
    
    async def update(self, goal_id: int, data: dict) -> Optional[GoalModel]:
        goal = await self.get_by_id(goal_id)
        if goal:
            for key, value in data.items():
                setattr(goal, key, value)
            await self.session.commit()
            await self.session.refresh(goal)
        return goal
    
    async def delete(self, goal_id: int) -> bool:
        goal = await self.get_by_id(goal_id)
        if goal:
            await self.session.delete(goal)
            await self.session.commit()
            return True
        return False