from typing import List, Optional
from app.modules.objectives.schemas.weekly_goal_schema import WeeklyGoalCreate, WeeklyGoalUpdate, WeeklyGoalResponse
from app.modules.objectives.implementation.weekly_goal_repository import WeeklyGoalRepository

class WeeklyGoalService:
    def __init__(self, repo: WeeklyGoalRepository):
        self.repo = repo
    
    async def get_all(self) -> List[WeeklyGoalResponse]:
        goals = await self.repo.get_all()
        return [WeeklyGoalResponse.model_validate(g) for g in goals]
    
    async def get_by_id(self, goal_id: int) -> WeeklyGoalResponse:
        goal = await self.repo.get_by_id(goal_id)
        if not goal:
            raise ValueError("Objetivo semanal no encontrado")
        return WeeklyGoalResponse.model_validate(goal)
    
    async def create(self, data: WeeklyGoalCreate) -> WeeklyGoalResponse:
        goal = await self.repo.create({
            "id_usuarios": data.id_usuarios,
            "opcion_1": data.opcion_1,
            "tiempo": data.tiempo,
            "opcion_2": data.opcion_2,
            "opcion_3": data.opcion_3,
            "fecha_limite": data.fecha_limite
        })
        return WeeklyGoalResponse.model_validate(goal)
    
    async def update(self, goal_id: int, data: WeeklyGoalUpdate) -> WeeklyGoalResponse:
        goal = await self.repo.get_by_id(goal_id)
        if not goal:
            raise ValueError("Objetivo semanal no encontrado")
        
        update_data = {}
        if data.opcion_1 is not None:
            update_data["opcion_1"] = data.opcion_1
        if data.tiempo is not None:
            update_data["tiempo"] = data.tiempo
        if data.opcion_2 is not None:
            update_data["opcion_2"] = data.opcion_2
        if data.opcion_3 is not None:
            update_data["opcion_3"] = data.opcion_3
        if data.fecha_limite is not None:
            update_data["fecha_limite"] = data.fecha_limite
            
        updated_goal = await self.repo.update(goal_id, update_data)
        return WeeklyGoalResponse.model_validate(updated_goal)
    
    async def delete(self, goal_id: int) -> bool:
        goal = await self.repo.get_by_id(goal_id)
        if not goal:
            raise ValueError("Objetivo semanal no encontrado")
        
        return await self.repo.delete(goal_id)