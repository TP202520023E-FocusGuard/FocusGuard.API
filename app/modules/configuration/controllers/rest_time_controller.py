from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.configuration.services.rest_time_service import RestTimeService
from app.modules.configuration.schemas.rest_time_schema import (
    RestTimeResponse,
    RestTimeUpdate
)

router = APIRouter(prefix="/rest-time", tags=["rest-time"])


@router.get("/{user_id}", response_model=RestTimeResponse)
async def get_tiempo_descanso(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtiene el tiempo de descanso del usuario"""
    try:
        service = RestTimeService(db)
        return await service.get_tiempo_descanso(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo tiempo de descanso: {str(e)}"
        )


@router.put("/{user_id}", response_model=RestTimeResponse)
async def update_tiempo_descanso(
    user_id: int,
    tiempo_update: RestTimeUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Actualiza el tiempo de descanso del usuario"""
    try:
        service = RestTimeService(db)
        return await service.update_tiempo_descanso(user_id, tiempo_update)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error actualizando tiempo de descanso: {str(e)}"
        )