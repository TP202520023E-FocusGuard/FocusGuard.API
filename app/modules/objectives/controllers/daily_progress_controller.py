from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.modules.objectives.services.daily_progress_service import DailyProgressService
from app.modules.objectives.schemas.daily_progress_schema import DailyProgressCreate, DailyProgressUpdate, DailyProgressResponse
from app.modules.objectives.implementation.daily_progress_repository import DailyProgressRepository
from app.modules.objectives.services.weekly_goal_service import WeeklyGoalService
from app.modules.objectives.implementation.weekly_goal_repository import WeeklyGoalRepository

router = APIRouter(prefix="/daily-progress", tags=["daily_progress"])

async def get_service(db: AsyncSession = Depends(get_db)) -> DailyProgressService:
    repo = DailyProgressRepository(db_session=db)
    return DailyProgressService(repo=repo)

async def get_weekly_goal_service(db: AsyncSession = Depends(get_db)) -> WeeklyGoalService:
    repo = WeeklyGoalRepository(db_session=db)
    return WeeklyGoalService(repo=repo)

@router.get("/", response_model=List[DailyProgressResponse])
async def get_all_daily_progress(service: DailyProgressService = Depends(get_service)):
    """
    Obtiene todos los registros de progreso diario.
    """
    return await service.get_all()

@router.get("/{progress_id}", response_model=DailyProgressResponse)
async def get_daily_progress_by_id(progress_id: int, service: DailyProgressService = Depends(get_service)):
    """
    Obtiene un registro de progreso diario por ID.
    """
    try:
        return await service.get_by_id(progress_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=DailyProgressResponse)
async def create_daily_progress(data: DailyProgressCreate, service: DailyProgressService = Depends(get_service)):
    """
    Crea un nuevo registro de progreso diario.
    """
    return await service.create(data)

@router.put("/{progress_id}", response_model=DailyProgressResponse)
async def update_daily_progress(progress_id: int, data: DailyProgressUpdate, service: DailyProgressService = Depends(get_service)):
    """
    Actualiza un registro de progreso diario existente.
    """
    try:
        return await service.update(progress_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{progress_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_daily_progress(progress_id: int, service: DailyProgressService = Depends(get_service)):
    """
    Elimina un registro de progreso diario.
    """
    try:
        success = await service.delete(progress_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de progreso diario no encontrado")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/weekly-goal/{goal_id}", response_model=List[DailyProgressResponse])
async def get_progress_by_weekly_goal(goal_id: int, service: DailyProgressService = Depends(get_service)):
    """
    Obtiene todos los progresos diarios de un objetivo semanal específico.
    """
    return await service.get_by_weekly_goal(goal_id)

@router.get("/weekly-goal/{goal_id}/today", response_model=Optional[DailyProgressResponse])
async def get_today_progress(goal_id: int, service: DailyProgressService = Depends(get_service)):
    """
    Obtiene el progreso de HOY para un objetivo semanal específico.
    """
    return await service.get_today_status(goal_id)

@router.post("/weekly-goal/{goal_id}/register")
async def register_today_progress(
    goal_id: int, 
    tiempo_usado: int,
    daily_service: DailyProgressService = Depends(get_service),
    weekly_service: WeeklyGoalService = Depends(get_weekly_goal_service)
):
    """
    Registra el progreso de hoy para un objetivo semanal.
    Calcula automáticamente si se alcanzó el objetivo.
    """
    try:
        weekly_goal = await weekly_service.get_by_id(goal_id)
        
        progress = await daily_service.register_daily_progress(goal_id, tiempo_usado, weekly_goal)
        return progress
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/weekly-goal/{goal_id}/summary")
async def get_weekly_summary(goal_id: int, service: DailyProgressService = Depends(get_service)):
    """
    Obtiene un resumen semanal del progreso de un objetivo.
    """
    try:
        summary = await service.get_weekly_summary(goal_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/register")
async def register_progress_simple(
    goal_id: int,
    tiempo_usado: int,
    daily_service: DailyProgressService = Depends(get_service),
    weekly_service: WeeklyGoalService = Depends(get_weekly_goal_service)
):
    """
    Endpoint simplificado para registrar progreso diario.
    """
    try:
        weekly_goal = await weekly_service.get_by_id(goal_id)
        progress = await daily_service.register_daily_progress(goal_id, tiempo_usado, weekly_goal)
        
        return {
            "message": "Progreso registrado exitosamente",
            "progress": progress,
            "goal_achieved": progress.es_alcanzado
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))