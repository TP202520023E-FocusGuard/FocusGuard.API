from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.modules.objectives.models.weekly_goal_model import WeeklyGoalModel

class WeeklyGoalRepository:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session
    
    async def get_all(self) -> List[WeeklyGoalModel]:
        stmt = select(WeeklyGoalModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, goal_id: int) -> Optional[WeeklyGoalModel]:
        stmt = select(WeeklyGoalModel).where(WeeklyGoalModel.id == goal_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(self, data: dict) -> WeeklyGoalModel:
        nuevo_objetivo = WeeklyGoalModel(**data)
        self.session.add(nuevo_objetivo)
        await self.session.commit()
        await self.session.refresh(nuevo_objetivo)
        return nuevo_objetivo
    
    async def update(self, goal_id: int, data: dict) -> Optional[WeeklyGoalModel]:
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
    
    async def get_by_user(self, user_id: int) -> List[WeeklyGoalModel]:
        stmt = select(WeeklyGoalModel).where(
            WeeklyGoalModel.id_usuarios == user_id
        ).order_by(WeeklyGoalModel.fecha_limite.asc())

        result = await self.session.execute(stmt)
        return result.scalars().all()