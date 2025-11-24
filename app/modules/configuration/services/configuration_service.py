from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.configuration.implementation.configuration_repository import ConfigurationRepository
from app.modules.configuration.schemas.configuration_schema import ConfigurationResponse, ConfigurationUpdate

class ConfigurationService:
    def __init__(self, session: AsyncSession):
        self.repository = ConfigurationRepository(session)
    
    async def get_configuration(self, user_id: int) -> ConfigurationResponse:
        """Obtiene la configuración del usuario, crea una por defecto si no existe"""
        config = await self.repository.get_user_configuration(user_id)
        
        if not config:
            # Crear configuración por defecto para usuario nuevo
            config = await self.repository.create_user_configuration(user_id)
        
        return ConfigurationResponse.model_validate(config)
    
    async def update_configuration(
        self, 
        user_id: int, 
        config_update: ConfigurationUpdate
    ) -> ConfigurationResponse:
        """Actualiza la configuración del usuario"""
        updated_config = await self.repository.update_user_configuration(user_id, config_update)
        
        if not updated_config:
            # Si no existe, crear primero
            await self.repository.create_user_configuration(user_id)
            updated_config = await self.repository.update_user_configuration(user_id, config_update)
        
        return ConfigurationResponse.model_validate(updated_config)