from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional
from app.modules.configuration.models.configuration_model import ConfigurationModel
from app.modules.configuration.schemas.configuration_schema import ConfigurationUpdate

class ConfigurationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_user_configuration(self, user_id: int) -> Optional[ConfigurationModel]:
        result = await self.session.execute(
            select(ConfigurationModel)
            .where(ConfigurationModel.id_usuario == user_id)
        )
        return result.scalar_one_or_none()
    
    async def create_user_configuration(self, user_id: int) -> ConfigurationModel:
        """Crea configuración por defecto para un usuario nuevo"""
        new_config = ConfigurationModel(
            id_usuario=user_id,
            tiempo_ocio_diario=120,
            tiempo_max_productivo=60,
            idioma='es',
            bloqueo_automatico=True
        )
        self.session.add(new_config)
        await self.session.commit()
        await self.session.refresh(new_config)
        return new_config
    
    async def update_user_configuration(
        self, 
        user_id: int, 
        config_update: ConfigurationUpdate
    ) -> Optional[ConfigurationModel]:
        # Actualizar solo los campos proporcionados
        update_data = {k: v for k, v in config_update.model_dump().items() if v is not None}
        
        if not update_data:
            return await self.get_user_configuration(user_id)
        
        await self.session.execute(
            update(ConfigurationModel)
            .where(ConfigurationModel.id_usuario == user_id)
            .values(**update_data)
        )
        await self.session.commit()
        
        return await self.get_user_configuration(user_id)