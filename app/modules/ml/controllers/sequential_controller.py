from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from app.core.database import get_db
from ..services.sequential_service import MLService
from ..implementation.sequential_repository import MLSequentialRepository
from ..schemas.sequential_schema import MLInputPayload
from app.core.exceptions import NotFoundException, DatabaseException

router = APIRouter(prefix="/sequential", tags=["sequential"])

def get_service(db: AsyncSession = Depends(get_db)) -> MLService:
    repo = MLSequentialRepository(db_session=db)
    return MLService(repo=repo)

@router.get(
    "/last10/{user_id}",
    response_model=MLInputPayload,
    summary="Obtiene los últimos 10 sitios visitados de un usuario para ML",
)
async def get_last_10_for_ml(
    user_id: int,
    service: MLService = Depends(get_service)
) -> Any:
    """
    Devuelve los últimos 10 sitios visitados de un usuario, con:
    - categoría vigente
    - tiempo de estancia
    """
    try:
        payload = await service.get_last_10_for_ml(user_id)
        return payload

    except NotFoundException as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except DatabaseException as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        # fallback genérico
        raise HTTPException(status_code=500, detail="Error inesperado")