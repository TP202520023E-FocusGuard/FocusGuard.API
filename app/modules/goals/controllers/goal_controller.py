from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.modules.goals.services.goal_service import GoalService
from app.modules.goals.schemas.goal_schema import GoalCreate, GoalUpdate, GoalResponse
from app.modules.goals.implementation.goal_repository import GoalRepository

router = APIRouter(prefix="/goals", tags=["goals"])

async def get_service(db: AsyncSession = Depends(get_db)) -> GoalService:
    repo = GoalRepository(db_session=db)
    return GoalService(repo=repo)

@router.get("/", response_model=List[GoalResponse])
async def get_all_goals(service: GoalService = Depends(get_service)):
    """
    Obtiene todas las metas.
    """
    return await service.get_all()

@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal_by_id(goal_id: int, service: GoalService = Depends(get_service)):
    """
    Obtiene una meta por ID.
    """
    try:
        return await service.get_by_id(goal_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/user/{user_id}", response_model=List[GoalResponse])
async def get_goals_by_user_id(user_id: int, service: GoalService = Depends(get_service)):
    """
    Obtiene las metas de un usuario por su ID.
    """
    return await service.get_by_user_id(user_id)

@router.post("/", response_model=GoalResponse)
async def create_goal(data: GoalCreate, service: GoalService = Depends(get_service)):
    """
    Crea una nueva meta.
    """
    return await service.create(data)

@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(goal_id: int, data: GoalUpdate, service: GoalService = Depends(get_service)):
    """
    Actualiza una meta existente.
    """
    try:
        return await service.update(goal_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(goal_id: int, service: GoalService = Depends(get_service)):
    """
    Elimina una meta.
    """
    try:
        success = await service.delete(goal_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta no encontrada")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))