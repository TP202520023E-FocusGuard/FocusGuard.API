from typing import List, Optional
from datetime import datetime, timedelta
from app.modules.objectives.schemas.daily_progress_schema import DailyProgressCreate, DailyProgressUpdate, DailyProgressResponse
from app.modules.objectives.implementation.daily_progress_repository import DailyProgressRepository

class DailyProgressService:
    def __init__(self, repo: DailyProgressRepository):
        self.repo = repo
    
    # MÉTODOS CRUD BÁSICOS
    async def get_all(self) -> List[DailyProgressResponse]:
        progress_records = await self.repo.get_all()
        return [DailyProgressResponse.model_validate(p) for p in progress_records]
    
    async def get_by_id(self, progress_id: int) -> DailyProgressResponse:
        progress = await self.repo.get_by_id(progress_id)
        if not progress:
            raise ValueError("Registro de progreso diario no encontrado")
        return DailyProgressResponse.model_validate(progress)
    
    async def create(self, data: DailyProgressCreate) -> DailyProgressResponse:
        progress = await self.repo.create({
            "id_objetivos_semanales": data.id_objetivos_semanales,
            "tiempo_alcanzado": data.tiempo_alcanzado,
            "es_alcanzado": data.es_alcanzado
        })
        return DailyProgressResponse.model_validate(progress)
    
    async def update(self, progress_id: int, data: DailyProgressUpdate) -> DailyProgressResponse:
        progress = await self.repo.get_by_id(progress_id)
        if not progress:
            raise ValueError("Registro de progreso diario no encontrado")
        
        update_data = {}
        if data.tiempo_alcanzado is not None:
            update_data["tiempo_alcanzado"] = data.tiempo_alcanzado
        if data.es_alcanzado is not None:
            update_data["es_alcanzado"] = data.es_alcanzado
            
        updated_progress = await self.repo.update(progress_id, update_data)
        return DailyProgressResponse.model_validate(updated_progress)
    
    async def delete(self, progress_id: int) -> bool:
        progress = await self.repo.get_by_id(progress_id)
        if not progress:
            raise ValueError("Registro de progreso diario no encontrado")
        
        return await self.repo.delete(progress_id)

    # NUEVOS MÉTODOS PRÁCTICOS
    async def get_by_weekly_goal(self, goal_id: int) -> List[DailyProgressResponse]:
        """Obtiene todos los progresos de un objetivo semanal"""
        progress_records = await self.repo.get_by_weekly_goal(goal_id)
        return [DailyProgressResponse.model_validate(p) for p in progress_records]

    async def get_today_status(self, goal_id: int) -> Optional[DailyProgressResponse]:
        """Obtiene el progreso de HOY para un objetivo específico"""
        today = datetime.now()
        progress = await self.repo.get_today_progress(goal_id, today)
        return DailyProgressResponse.model_validate(progress) if progress else None

    async def register_daily_progress(self, goal_id: int, tiempo_usado: int, weekly_goal) -> DailyProgressResponse:
        """
        Registra el progreso diario automáticamente calculando si se alcanzó el objetivo
        """
        # Calcular si se alcanzó el objetivo
        if weekly_goal.opcion_1 == 1:  # MÁS tiempo
            es_alcanzado = tiempo_usado >= weekly_goal.tiempo
        else:  # MENOS tiempo  
            es_alcanzado = tiempo_usado <= weekly_goal.tiempo
        
        # Verificar si ya existe registro para hoy
        today = datetime.now()
        existing_progress = await self.repo.get_today_progress(goal_id, today)
        
        if existing_progress:
            # Actualizar registro existente
            return await self.update(existing_progress.id, DailyProgressUpdate(
                tiempo_alcanzado=tiempo_usado,
                es_alcanzado=es_alcanzado
            ))
        else:
            # Crear nuevo registro
            return await self.create(DailyProgressCreate(
                id_objetivos_semanales=goal_id,
                tiempo_alcanzado=tiempo_usado,
                es_alcanzado=es_alcanzado
            ))

    async def get_weekly_summary(self, goal_id: int) -> dict:
        """
        Obtiene resumen semanal de un objetivo
        """
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        
        weekly_progress = await self.repo.get_weekly_progress(goal_id, start_date, end_date)
        
        total_days = len(weekly_progress)
        achieved_days = len([p for p in weekly_progress if p.es_alcanzado])
        
        return {
            "goal_id": goal_id,
            "total_days": total_days,
            "achieved_days": achieved_days,
            "success_rate": (achieved_days / total_days * 100) if total_days > 0 else 0,
            "progress_records": [DailyProgressResponse.model_validate(p) for p in weekly_progress]
        }