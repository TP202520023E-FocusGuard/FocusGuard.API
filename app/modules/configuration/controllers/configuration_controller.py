from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.configuration.services.configuration_service import ConfigurationService
from app.modules.configuration.schemas.configuration_schema import ConfigurationResponse, ConfigurationUpdate

router = APIRouter(prefix="/configuration", tags=["configuration"])

@router.get("/{user_id}", response_model=ConfigurationResponse)
async def get_configuration(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtiene la configuración del usuario"""
    try:
        service = ConfigurationService(db)
        return await service.get_configuration(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo configuración: {str(e)}"
        )

@router.put("/{user_id}", response_model=ConfigurationResponse)
async def update_configuration(
    user_id: int,
    config_update: ConfigurationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Actualiza la configuración del usuario"""
    try:
        service = ConfigurationService(db)
        return await service.update_configuration(user_id, config_update)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error actualizando configuración: {str(e)}"
        )