import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, update
from typing import Any, Dict, List, Optional
from app.modules.objectives.models.weekly_goal_model import WeeklyGoalModel
from datetime import timezone

class WeeklyGoalRepository:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session
    
    async def get_all(self) -> List[WeeklyGoalModel]:
        stmt = select(WeeklyGoalModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, goal_id: int) -> Optional[WeeklyGoalModel]:
        stmt = select(WeeklyGoalModel).where(WeeklyGoalModel.id == goal_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(self, data: dict) -> WeeklyGoalModel:
        # Lógica de estado inicial: 'Menos' (2) inicia en True, 'Mas' (1) en False
        if data.get('opcion_1') == 2:
            data['completado'] = True
        else:
            data['completado'] = False
            
        nuevo_objetivo = WeeklyGoalModel(**data)
        self.session.add(nuevo_objetivo)
        await self.session.commit()
        await self.session.refresh(nuevo_objetivo)
        return nuevo_objetivo

    async def update(self, goal_id: int, data: dict) -> Optional[WeeklyGoalModel]:
        goal = await self.get_by_id(goal_id)
        if goal:
            for key, value in data.items():
                setattr(goal, key, value)
            goal.fecha_modificacion = datetime.datetime.now(timezone.utc)
            await self.session.commit()
            await self.session.refresh(goal)
        return goal
    
    async def delete(self, goal_id: int) -> bool:
        goal = await self.get_by_id(goal_id)
        if goal:
            await self.session.delete(goal)
            await self.session.commit()
            return True
        return False
    
    async def get_by_user(self, user_id: int) -> List[WeeklyGoalModel]:
        stmt = select(WeeklyGoalModel).where(
            WeeklyGoalModel.id_usuarios == user_id
        ).order_by(WeeklyGoalModel.fecha_limite.asc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # --- MÉTODO DE SINCRONIZACIÓN Y PROGRESO ---

    async def _fetch_progress_data(self, user_id: int, goal_id: Optional[int] = None) -> List[Dict[str, Any]]:
        extra_filter = "AND os.id = :goal_id" if goal_id else ""
        
        query = text(f"""
            WITH TiemposCalculados AS (
                SELECT 
                    os.id, os.id_usuarios, os.opcion_1, os.tiempo AS meta_minutos,
                    os.opcion_2, os.opcion_3, os.fecha_inicio, os.fecha_limite,
                    os.completado AS completado_db, -- El valor actual en la tabla
                    CASE 
                        WHEN os.opcion_2 = 1 THEN (
                            SELECT COALESCE(SUM(ABS(TIMESTAMPDIFF(SECOND, swv.fecha_hora_ingreso, swv.fecha_hora_salida))), 0) / 60
                            FROM sitios_web_visitados swv
                            INNER JOIN categorias_web cw ON swv.id_categorias_web = cw.id
                            WHERE swv.id_usuarios = os.id_usuarios
                              AND cw.codigo = os.opcion_3
                              AND swv.fecha_hora_salida IS NOT NULL
                              AND swv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                        )
                        WHEN os.opcion_2 = 2 THEN (
                            SELECT COALESCE(SUM(ABS(TIMESTAMPDIFF(SECOND, cv.fecha_hora_ingreso, cv.fecha_hora_salida))), 0) / 60
                            FROM contenidos_visitados cv
                            INNER JOIN contenidos_usuario cu ON cv.id_contenidos_usuario = cu.id
                            INNER JOIN categorias_contenido cc ON cu.id_categorias_contenido = cc.id
                            WHERE cv.id_usuarios = os.id_usuarios
                              AND cc.nombre = os.opcion_3
                              AND cv.fecha_hora_salida IS NOT NULL
                              AND cv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                        )
                        ELSE 0
                    END AS tiempo_actual
                FROM objetivos_semanales os
                WHERE os.id_usuarios = :user_id
                {extra_filter}
                AND os.fecha_inicio >= DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY)
                AND os.fecha_inicio < DATE_ADD(DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY), INTERVAL 1 WEEK)
            )
            SELECT 
                id, opcion_1, opcion_2, opcion_3, fecha_inicio, fecha_limite,
                meta_minutos AS tiempo_objetivo,
                ROUND(tiempo_actual, 2) AS tiempo_actual,
                completado_db,
                CASE 
                    WHEN opcion_1 = 1 AND tiempo_actual >= meta_minutos THEN 1
                    WHEN opcion_1 = 2 AND tiempo_actual <= meta_minutos THEN 1
                    ELSE 0
                END AS completado_calculado,
                CASE 
                    WHEN meta_minutos = 0 THEN 100
                    ELSE LEAST(100, ROUND((tiempo_actual / meta_minutos) * 100, 2))
                END AS porcentaje_progreso
            FROM TiemposCalculados
            ORDER BY fecha_limite ASC
        """)
        
        params = {"user_id": user_id}
        if goal_id: params["goal_id"] = goal_id
        
        result = await self.session.execute(query, params)
        rows = result.fetchall()
        
        final_results = []
        sync_list = [] # Para guardar qué IDs necesitan actualizarse

        for row in rows:
            mapping = row._mapping
            calc_status = bool(mapping.completado_calculado)
            db_status = bool(mapping.completado_db)

            # Si el cálculo actual difiere de la DB, lo marcamos para sincronizar
            if calc_status != db_status:
                sync_list.append({"id": mapping.id, "completado": calc_status})

            final_results.append({
                "id": mapping.id,
                "opcion_1": mapping.opcion_1,
                "opcion_2": mapping.opcion_2,
                "opcion_3": mapping.opcion_3,
                "fecha_inicio": mapping.fecha_inicio,
                "fecha_limite": mapping.fecha_limite,
                "tiempo_objetivo": float(mapping.tiempo_objetivo),
                "tiempo_actual": float(mapping.tiempo_actual),
                "porcentaje_progreso": float(mapping.porcentaje_progreso),
                "completado": calc_status
            })

        # --- SINCRONIZACIÓN AUTOMÁTICA (Opcional pero óptimo) ---
        if sync_list:
            for item in sync_list:
                await self.session.execute(
                    update(WeeklyGoalModel)
                    .where(WeeklyGoalModel.id == item["id"])
                    .values(completado=item["completado"])
                )
            await self.session.commit()

        return final_results

    async def get_goals_progress(self, user_id: int) -> List[Dict[str, Any]]:
        return await self._fetch_progress_data(user_id)

    async def get_goal_progress(self, goal_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        results = await self._fetch_progress_data(user_id, goal_id)
        return results[0] if results else None