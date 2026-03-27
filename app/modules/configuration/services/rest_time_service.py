from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.configuration.implementation.rest_time_repository import RestTimeRepository
from app.modules.configuration.schemas.rest_time_schema import (
    RestTimeResponse,
    RestTimeUpdate
)

class RestTimeService:
    def __init__(self, session: AsyncSession):
        self.repository = RestTimeRepository(session)
    
    async def get_tiempo_descanso(self, user_id: int) -> RestTimeResponse:
        """Obtiene el tiempo de descanso del usuario, crea uno por defecto si no existe"""
        tiempo = await self.repository.get_by_user_id(user_id)
        
        if tiempo is None:
            tiempo = await self.repository.create(user_id)
        
        return RestTimeResponse.model_validate(tiempo)
    
    async def update_tiempo_descanso(
        self, 
        user_id: int, 
        tiempo_update: RestTimeUpdate
    ) -> RestTimeResponse:
        """Actualiza el tiempo de descanso del usuario"""
        existing = await self.repository.get_by_user_id(user_id)
        if not existing:
            raise ValueError("Usuario no encontrado")
        updated_tiempo = await self.repository.update_by_user_id(user_id, tiempo_update)
        return RestTimeResponse.model_validate(updated_tiempo)