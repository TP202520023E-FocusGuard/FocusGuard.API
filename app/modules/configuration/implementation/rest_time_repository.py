from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional
from datetime import date

from app.modules.configuration.models.rest_time_model import RestTimeModel
from app.modules.configuration.schemas.rest_time_schema import RestTimeUpdate


class RestTimeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_user_id(self, user_id: int) -> Optional[RestTimeModel]:
        result = await self.session.execute(
            select(RestTimeModel)
            .where(RestTimeModel.id_usuarios == user_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, user_id: int) -> RestTimeModel:
        """Crea registro por defecto para un usuario nuevo"""
        new_tiempo = RestTimeModel(
            id_usuarios=user_id,
            tiempo_total=60,  # puedes ajustar default
            tiempo_usado=0,
            fecha_actualizacion=date.today()
        )
        self.session.add(new_tiempo)
        await self.session.commit()
        await self.session.refresh(new_tiempo)
        return new_tiempo
    
    async def update_by_user_id(
        self, 
        user_id: int, 
        tiempo_update: RestTimeUpdate
    ) -> Optional[RestTimeModel]:
        
        update_data = {
            k: v for k, v in tiempo_update.model_dump().items() if v is not None
        }
        
        if not update_data:
            return await self.get_by_user_id(user_id)
        
        await self.session.execute(
            update(RestTimeModel)
            .where(RestTimeModel.id_usuarios == user_id)
            .values(**update_data)
        )
        await self.session.commit()
        
        return await self.get_by_user_id(user_id)
    
    async def reset_tiempo(self, user_id: int, today: date) -> Optional[RestTimeModel]:
        await self.session.execute(
            update(RestTimeModel)
            .where(RestTimeModel.id_usuarios == user_id)
            .values(
                tiempo_usado=0,
                fecha_actualizacion=today
            )
        )
        await self.session.commit()
        
        return await self.get_by_user_id(user_id)
    
    async def increment_time(self, user_id: int, minutos: int) -> Optional[RestTimeModel]:
        await self.session.execute(
            update(RestTimeModel)
            .where(RestTimeModel.id_usuarios == user_id)
            .values(
                tiempo_usado=RestTimeModel.tiempo_usado + minutos
            )
        )
        await self.session.commit()
        
        return await self.get_by_user_id(user_id)