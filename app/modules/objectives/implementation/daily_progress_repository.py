from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime
from app.modules.objectives.models.daily_progress_model import DailyProgressModel

class DailyProgressRepository:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session
    
    async def get_all(self) -> List[DailyProgressModel]:
        stmt = select(DailyProgressModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, progress_id: int) -> Optional[DailyProgressModel]:
        stmt = select(DailyProgressModel).where(DailyProgressModel.id == progress_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(self, data: dict) -> DailyProgressModel:
        nuevo_progreso = DailyProgressModel(**data)
        self.session.add(nuevo_progreso)
        await self.session.commit()
        await self.session.refresh(nuevo_progreso)
        return nuevo_progreso
    
    async def update(self, progress_id: int, data: dict) -> Optional[DailyProgressModel]:
        progress = await self.get_by_id(progress_id)
        if progress:
            for key, value in data.items():
                setattr(progress, key, value)
            await self.session.commit()
            await self.session.refresh(progress)
        return progress
    
    async def delete(self, progress_id: int) -> bool:
        progress = await self.get_by_id(progress_id)
        if progress:
            await self.session.delete(progress)
            await self.session.commit()
            return True
        return False

    # NUEVOS MÉTODOS PRÁCTICOS
    async def get_by_weekly_goal(self, goal_id: int) -> List[DailyProgressModel]:
        stmt = select(DailyProgressModel).where(
            DailyProgressModel.id_objetivos_semanales == goal_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_today_progress(self, goal_id: int, target_date: datetime) -> Optional[DailyProgressModel]:
        stmt = select(DailyProgressModel).where(
            DailyProgressModel.id_objetivos_semanales == goal_id,
            func.date(DailyProgressModel.fecha) == target_date.date()
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_weekly_progress(self, goal_id: int, start_date: datetime, end_date: datetime) -> List[DailyProgressModel]:
        stmt = select(DailyProgressModel).where(
            DailyProgressModel.id_objetivos_semanales == goal_id,
            DailyProgressModel.fecha >= start_date,
            DailyProgressModel.fecha <= end_date
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()