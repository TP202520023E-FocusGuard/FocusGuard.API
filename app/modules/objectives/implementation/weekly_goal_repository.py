import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from typing import Any, Dict, List, Optional
from app.modules.objectives.models.weekly_goal_model import WeeklyGoalModel

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
            goal.fecha_modificacion = datetime.datetime.now()
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
    
    async def mark_as_completed(self, goal_id: int) -> Optional[WeeklyGoalModel]:
        goal = await self.get_by_id(goal_id)
        if goal:
            goal.completado = True
            goal.fecha_modificacion = datetime.datetime.now()
            await self.session.commit()
            await self.session.refresh(goal)
        return goal
    
    # METODO PARA MEDIR PROGRESO

    async def get_goals_progress(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene todos los objetivos del usuario con su progreso actual
        """
        query = text("""
            SELECT 
                os.id,
                os.id_usuarios,
                os.opcion_1,
                os.tiempo as tiempo_objetivo,
                os.opcion_2,
                os.opcion_3,
                os.fecha_inicio,
                os.fecha_limite,
                os.completado as completado_manual,
                
                -- Tiempo actual
                CASE 
                    WHEN os.opcion_2 = 1 THEN (
                        SELECT COALESCE(SUM(TIMESTAMPDIFF(MINUTE, swv.fecha_hora_ingreso, swv.fecha_hora_salida)), 0)
                        FROM sitios_web_visitados swv
                        INNER JOIN categorias_web cw ON swv.id_categorias_web = cw.id
                        WHERE swv.id_usuarios = os.id_usuarios
                          AND cw.codigo = os.opcion_3
                          AND swv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                    )
                    WHEN os.opcion_2 = 2 THEN (
                        SELECT COALESCE(SUM(TIMESTAMPDIFF(MINUTE, cv.fecha_hora_ingreso, cv.fecha_hora_salida)), 0)
                        FROM contenidos_visitados cv
                        INNER JOIN contenidos_usuario cu ON cv.id_contenidos_usuario = cu.id
                        INNER JOIN categorias_contenido cc ON cu.id_categorias_contenido = cc.id
                        WHERE cv.id_usuarios = os.id_usuarios
                          AND cc.nombre = os.opcion_3
                          AND cv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                    )
                END as tiempo_actual,
                
                -- Completado (según opcion_1)
                CASE 
                    WHEN os.completado = 1 THEN 1
                    WHEN os.opcion_1 = 1 THEN 
                        CASE 
                            WHEN (
                                CASE 
                                    WHEN os.opcion_2 = 1 THEN (
                                        SELECT COALESCE(SUM(TIMESTAMPDIFF(MINUTE, swv.fecha_hora_ingreso, swv.fecha_hora_salida)), 0)
                                        FROM sitios_web_visitados swv
                                        INNER JOIN categorias_web cw ON swv.id_categorias_web = cw.id
                                        WHERE swv.id_usuarios = os.id_usuarios
                                          AND cw.codigo = os.opcion_3
                                          AND swv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                                    )
                                    WHEN os.opcion_2 = 2 THEN (
                                        SELECT COALESCE(SUM(TIMESTAMPDIFF(MINUTE, cv.fecha_hora_ingreso, cv.fecha_hora_salida)), 0)
                                        FROM contenidos_visitados cv
                                        INNER JOIN contenidos_usuario cu ON cv.id_contenidos_usuario = cu.id
                                        INNER JOIN categorias_contenido cc ON cu.id_categorias_contenido = cc.id
                                        WHERE cv.id_usuarios = os.id_usuarios
                                          AND cc.nombre = os.opcion_3
                                          AND cv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                                    )
                                END
                            ) >= os.tiempo THEN 1 ELSE 0
                        END
                    WHEN os.opcion_1 = 2 THEN 
                        CASE 
                            WHEN (
                                CASE 
                                    WHEN os.opcion_2 = 1 THEN (
                                        SELECT COALESCE(SUM(TIMESTAMPDIFF(MINUTE, swv.fecha_hora_ingreso, swv.fecha_hora_salida)), 0)
                                        FROM sitios_web_visitados swv
                                        INNER JOIN categorias_web cw ON swv.id_categorias_web = cw.id
                                        WHERE swv.id_usuarios = os.id_usuarios
                                          AND cw.codigo = os.opcion_3
                                          AND swv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                                    )
                                    WHEN os.opcion_2 = 2 THEN (
                                        SELECT COALESCE(SUM(TIMESTAMPDIFF(MINUTE, cv.fecha_hora_ingreso, cv.fecha_hora_salida)), 0)
                                        FROM contenidos_visitados cv
                                        INNER JOIN contenidos_usuario cu ON cv.id_contenidos_usuario = cu.id
                                        INNER JOIN categorias_contenido cc ON cu.id_categorias_contenido = cc.id
                                        WHERE cv.id_usuarios = os.id_usuarios
                                          AND cc.nombre = os.opcion_3
                                          AND cv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                                    )
                                END
                            ) <= os.tiempo THEN 1 ELSE 0
                        END
                END as completado,
                
                -- Porcentaje de progreso
                CASE 
                    WHEN os.opcion_1 = 1 THEN 
                        LEAST(100, ROUND(
                            (
                                CASE 
                                    WHEN os.opcion_2 = 1 THEN (
                                        SELECT COALESCE(SUM(TIMESTAMPDIFF(MINUTE, swv.fecha_hora_ingreso, swv.fecha_hora_salida)), 0)
                                        FROM sitios_web_visitados swv
                                        INNER JOIN categorias_web cw ON swv.id_categorias_web = cw.id
                                        WHERE swv.id_usuarios = os.id_usuarios
                                          AND cw.codigo = os.opcion_3
                                          AND swv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                                    )
                                    WHEN os.opcion_2 = 2 THEN (
                                        SELECT COALESCE(SUM(TIMESTAMPDIFF(MINUTE, cv.fecha_hora_ingreso, cv.fecha_hora_salida)), 0)
                                        FROM contenidos_visitados cv
                                        INNER JOIN contenidos_usuario cu ON cv.id_contenidos_usuario = cu.id
                                        INNER JOIN categorias_contenido cc ON cu.id_categorias_contenido = cc.id
                                        WHERE cv.id_usuarios = os.id_usuarios
                                          AND cc.nombre = os.opcion_3
                                          AND cv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                                    )
                                END
                            ) / os.tiempo * 100
                        ))
                    WHEN os.opcion_1 = 2 THEN 
                        LEAST(100, ROUND(
                            (
                                CASE 
                                    WHEN os.opcion_2 = 1 THEN (
                                        SELECT COALESCE(SUM(TIMESTAMPDIFF(MINUTE, swv.fecha_hora_ingreso, swv.fecha_hora_salida)), 0)
                                        FROM sitios_web_visitados swv
                                        INNER JOIN categorias_web cw ON swv.id_categorias_web = cw.id
                                        WHERE swv.id_usuarios = os.id_usuarios
                                          AND cw.codigo = os.opcion_3
                                          AND swv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                                    )
                                    WHEN os.opcion_2 = 2 THEN (
                                        SELECT COALESCE(SUM(TIMESTAMPDIFF(MINUTE, cv.fecha_hora_ingreso, cv.fecha_hora_salida)), 0)
                                        FROM contenidos_visitados cv
                                        INNER JOIN contenidos_usuario cu ON cv.id_contenidos_usuario = cu.id
                                        INNER JOIN categorias_contenido cc ON cu.id_categorias_contenido = cc.id
                                        WHERE cv.id_usuarios = os.id_usuarios
                                          AND cc.nombre = os.opcion_3
                                          AND cv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                                    )
                                END
                            ) / os.tiempo * 100
                        ))
                END as porcentaje_progreso
                
            FROM objetivos_semanales os
            WHERE os.id_usuarios = :user_id
              AND os.fecha_limite >= NOW()
            ORDER BY os.fecha_limite ASC
        """)
        
        result = await self.session.execute(query, {"user_id": user_id})
        rows = result.fetchall()
        
        goals_with_progress = []
        for row in rows:
            goal = dict(row._mapping)
            
            goals_with_progress.append({
                "id": goal['id'],
                "opcion_1": goal['opcion_1'],
                "opcion_2": goal['opcion_2'],
                "opcion_3": goal['opcion_3'],
                "tiempo_objetivo": goal['tiempo_objetivo'],
                "tiempo_actual": goal['tiempo_actual'],
                "fecha_inicio": goal['fecha_inicio'],
                "fecha_limite": goal['fecha_limite'],
                "completado": goal['completado'] == 1,
                "porcentaje_progreso": goal['porcentaje_progreso']
            })
        
        return goals_with_progress


    async def get_goal_progress(self, goal_id: int, user_id: int) -> Dict[str, Any]:
        """
        Obtiene el progreso de un objetivo específico
        """
        query = text("""
            SELECT 
                os.id,
                os.id_usuarios,
                os.opcion_1,
                os.tiempo as tiempo_objetivo,
                os.opcion_2,
                os.opcion_3,
                os.fecha_inicio,
                os.fecha_limite,
                os.completado,
                COALESCE(
                    CASE 
                        WHEN os.opcion_2 = 1 THEN (
                            SELECT SUM(TIMESTAMPDIFF(MINUTE, swv.fecha_hora_ingreso, swv.fecha_hora_salida))
                            FROM sitios_web_visitados swv
                            INNER JOIN sitios_web_usuario swu ON swv.id_sitios_web_usuario = swu.id
                            INNER JOIN categorias_web cw ON swu.id_categorias_web = cw.id
                            WHERE swv.id_usuarios = os.id_usuarios
                            AND cw.codigo = os.opcion_3
                            AND swv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                        )
                        WHEN os.opcion_2 = 2 THEN (
                            SELECT SUM(TIMESTAMPDIFF(MINUTE, cv.fecha_hora_ingreso, cv.fecha_hora_salida))
                            FROM contenidos_visitados cv
                            INNER JOIN contenidos_usuario cu ON cv.id_contenidos_usuario = cu.id
                            INNER JOIN categorias_contenido cc ON cu.id_categorias_contenido = cc.id
                            WHERE cv.id_usuarios = os.id_usuarios
                            AND cc.nombre = os.opcion_3
                            AND cv.fecha_hora_ingreso BETWEEN os.fecha_inicio AND os.fecha_limite
                        )
                    END, 0
                ) as tiempo_actual
            FROM objetivos_semanales os
            WHERE os.id = :goal_id AND os.id_usuarios = :user_id
        """)
        
        result = await self.session.execute(query, {"goal_id": goal_id, "user_id": user_id})
        row = result.fetchone()
        
        if not row:
            return None
        
        goal = dict(row._mapping)
        
        tiempo_actual = goal.get('tiempo_actual', 0)
        tiempo_objetivo = goal.get('tiempo_objetivo', 0)
        completado = goal.get('completado', False)
        
        # Calcular porcentaje según tipo de objetivo
        if tiempo_objetivo > 0:
            if completado:
                porcentaje = 100
            else:
                if goal['opcion_1'] == 1:  # MÁS
                    porcentaje = min(99, int((tiempo_actual / tiempo_objetivo) * 100))
                else:  # MENOS
                    porcentaje = min(99, int((tiempo_actual / tiempo_objetivo) * 100))
        else:
            porcentaje = 0
        
        return {
            "id": goal['id'],
            "opcion_1": goal['opcion_1'],
            "opcion_2": goal['opcion_2'],
            "opcion_3": goal['opcion_3'],
            "tiempo_objetivo": tiempo_objetivo,
            "tiempo_actual": tiempo_actual,
            "fecha_inicio": goal['fecha_inicio'],
            "fecha_limite": goal['fecha_limite'],
            "completado": completado,  # Directamente de la BD
            "porcentaje_progreso": porcentaje
        }