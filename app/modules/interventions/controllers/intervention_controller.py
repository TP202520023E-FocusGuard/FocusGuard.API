from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from ..implementation.intervention_repository import InterventionRepository
from ..schemas.intervention_schema import (
    IntAvisoCreate,
    IntAvisoResponse,
    IntBloqueoCreate,
    IntBloqueoResponse,
    IntEscrituraCreate,
    IntEscrituraResponse,
    InterventionCreate,
    InterventionResponse,
    InterventionUpdateUnlockDate,
)
from ..services.intervention_service import InterventionService


router = APIRouter(prefix="/interventions", tags=["interventions"])


def get_service(db: AsyncSession = Depends(get_db)) -> InterventionService:
    repo = InterventionRepository(db_session=db)
    return InterventionService(repo=repo)


@router.post("/", response_model=InterventionResponse, status_code=status.HTTP_201_CREATED)
async def create_intervention(
    data: InterventionCreate,
    service: InterventionService = Depends(get_service),
) -> InterventionResponse:
    return await service.create_intervention(data)


@router.get("/{intervention_id}", response_model=InterventionResponse)
async def get_intervention_by_id(
    intervention_id: int,
    service: InterventionService = Depends(get_service),
) -> InterventionResponse:
    try:
        return await service.get_intervention_by_id(intervention_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/user/{user_id}/today-count")
async def get_today_count_by_user(
    user_id: int,
    service: InterventionService = Depends(get_service),
) -> dict:
    cantidad = await service.get_today_count_by_user(user_id)
    return {"id_usuarios": user_id, "cantidad_hoy": cantidad}


@router.get("/user/{user_id}/last-today", response_model=InterventionResponse | None)
async def get_last_intervention_by_user_if_today(
    user_id: int,
    service: InterventionService = Depends(get_service),
) -> InterventionResponse | None:
    return await service.get_last_by_user_if_today(user_id)


@router.get("/user/{user_id}", response_model=list[InterventionResponse])
async def get_interventions_by_user(
    user_id: int,
    service: InterventionService = Depends(get_service),
) -> list[InterventionResponse]:
    return await service.get_interventions_by_user(user_id)


@router.patch("/{intervention_id}", response_model=InterventionResponse)
async def update_intervention_unlock_date(
    intervention_id: int,
    data: InterventionUpdateUnlockDate,
    service: InterventionService = Depends(get_service),
) -> InterventionResponse:
    try:
        return await service.update_unlock_date(intervention_id, data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{intervention_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_intervention_by_id(
    intervention_id: int,
    service: InterventionService = Depends(get_service),
) -> None:
    try:
        await service.delete_intervention_by_id(intervention_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/int-avisos", response_model=IntAvisoResponse, status_code=status.HTTP_201_CREATED)
async def create_int_aviso(
    data: IntAvisoCreate,
    service: InterventionService = Depends(get_service),
) -> IntAvisoResponse:
    return await service.create_int_aviso(data)


@router.delete("/int-avisos/{intervention_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_int_aviso_by_pk(
    intervention_id: int,
    service: InterventionService = Depends(get_service),
) -> None:
    try:
        await service.delete_int_aviso_by_pk(intervention_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/int-bloqueos", response_model=IntBloqueoResponse, status_code=status.HTTP_201_CREATED)
async def create_int_bloqueo(
    data: IntBloqueoCreate,
    service: InterventionService = Depends(get_service),
) -> IntBloqueoResponse:
    return await service.create_int_bloqueo(data)


@router.delete("/int-bloqueos/{intervention_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_int_bloqueo_by_pk(
    intervention_id: int,
    service: InterventionService = Depends(get_service),
) -> None:
    try:
        await service.delete_int_bloqueo_by_pk(intervention_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/int-escrituras", response_model=IntEscrituraResponse, status_code=status.HTTP_201_CREATED)
async def create_int_escritura(
    data: IntEscrituraCreate,
    service: InterventionService = Depends(get_service),
) -> IntEscrituraResponse:
    return await service.create_int_escritura(data)


@router.delete("/int-escrituras/{intervention_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_int_escritura_by_pk(
    intervention_id: int,
    service: InterventionService = Depends(get_service),
) -> None:
    try:
        await service.delete_int_escritura_by_pk(intervention_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc