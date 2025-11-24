from typing import List, Optional
from app.modules.goals.schemas.goal_schema import GoalCreate, GoalUpdate, GoalResponse
from app.modules.goals.implementation.goal_repository import GoalRepository

class GoalService:
    def __init__(self, repo: GoalRepository):
        self.repo = repo
    
    async def get_all(self) -> List[GoalResponse]:
        goals = await self.repo.get_all()
        return [GoalResponse.model_validate(g) for g in goals]
    
    async def get_by_id(self, goal_id: int) -> GoalResponse:
        goal = await self.repo.get_by_id(goal_id)
        if not goal:
            raise ValueError("Meta no encontrada")
        return GoalResponse.model_validate(goal)
    
    async def get_by_user_id(self, user_id: int) -> List[GoalResponse]:
        goals = await self.repo.get_by_user_id(user_id)
        return [GoalResponse.model_validate(g) for g in goals]

    async def create(self, data: GoalCreate) -> GoalResponse:
        goal = await self.repo.create({
            "id_usuarios": data.id_usuarios,
            "texto": data.texto
        })
        return GoalResponse.model_validate(goal)
    
    async def update(self, goal_id: int, data: GoalUpdate) -> GoalResponse:
        goal = await self.repo.get_by_id(goal_id)
        if not goal:
            raise ValueError("Meta no encontrada")
        
        update_data = {}
        if data.texto is not None:
            update_data["texto"] = data.texto
            
        updated_goal = await self.repo.update(goal_id, update_data)
        return GoalResponse.model_validate(updated_goal)
    
    async def delete(self, goal_id: int) -> bool:
        goal = await self.repo.get_by_id(goal_id)
        if not goal:
            raise ValueError("Meta no encontrada")
        
        return await self.repo.delete(goal_id)