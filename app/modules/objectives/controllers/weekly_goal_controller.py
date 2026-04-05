from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.modules.objectives.services.weekly_goal_service import WeeklyGoalService
from app.modules.objectives.schemas.weekly_goal_schema import WeeklyGoalCreate, WeeklyGoalUpdate, WeeklyGoalResponse
from app.modules.objectives.implementation.weekly_goal_repository import WeeklyGoalRepository

router = APIRouter(prefix="/weekly-goals", tags=["weekly_goals"])

async def get_service(db: AsyncSession = Depends(get_db)) -> WeeklyGoalService:
    repo = WeeklyGoalRepository(db_session=db)
    return WeeklyGoalService(repo=repo)

@router.get("/", response_model=List[WeeklyGoalResponse])
async def get_all_weekly_goals(service: WeeklyGoalService = Depends(get_service)):
    """
    Obtiene todos los objetivos semanales.
    """
    return await service.get_all()

@router.get("/{goal_id}", response_model=WeeklyGoalResponse)
async def get_weekly_goal_by_id(goal_id: int, service: WeeklyGoalService = Depends(get_service)):
    """
    Obtiene un objetivo semanal por ID.
    """
    try:
        return await service.get_by_id(goal_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=WeeklyGoalResponse)
async def create_weekly_goal(data: WeeklyGoalCreate, service: WeeklyGoalService = Depends(get_service)):
    """
    Crea un nuevo objetivo semanal.
    """
    return await service.create(data)

@router.put("/{goal_id}", response_model=WeeklyGoalResponse)
async def update_weekly_goal(goal_id: int, data: WeeklyGoalUpdate, service: WeeklyGoalService = Depends(get_service)):
    """
    Actualiza un objetivo semanal existente.
    """
    try:
        return await service.update(goal_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_weekly_goal(goal_id: int, service: WeeklyGoalService = Depends(get_service)):
    """
    Elimina un objetivo semanal.
    """
    try:
        success = await service.delete(goal_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objetivo semanal no encontrado")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.get("/user/{user_id}", response_model=List[WeeklyGoalResponse])
async def get_weekly_goals_by_user(
    user_id: int,
    service: WeeklyGoalService = Depends(get_service)
):
    """
    Obtiene todos los objetivos semanales de un usuario.
    """
    goals = await service.get_by_user(user_id)
    return goals
