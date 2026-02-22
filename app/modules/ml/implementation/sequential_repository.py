from __future__ import annotations
from app.core.exceptions import DatabaseException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class MLSequentialRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def get_last_10_for_ml(self, user_id: int) -> List[dict]:
        try:
            query = text("""
                SELECT
                    COALESCE(
                        (SELECT nombre FROM categorias_web cw WHERE cw.id = COALESCE(
                            (SELECT c.id_categorias_web_nuevo FROM cambios_categoria c 
                             WHERE c.id_usuarios = v.id_usuarios 
                             AND c.id_sitios_web_usuario = v.id_sitios_web_usuario 
                             AND c.fecha_hora <= v.fecha_hora_salida 
                             ORDER BY c.fecha_hora DESC LIMIT 1),
                            (SELECT s.id_categorias_web FROM sitios_web_usuario s WHERE s.id = v.id_sitios_web_usuario)
                        )), 'Desconocida'
                    ) AS categoria_nombre,
                    /* Como filtramos NOT NULL, el cálculo es más directo */
                    GREATEST(0, TIMESTAMPDIFF(SECOND, v.fecha_hora_ingreso, v.fecha_hora_salida)) AS duracion_segundos
                FROM sitios_web_visitados v
                WHERE v.id_usuarios = :user_id 
                  AND v.fecha_hora_salida IS NOT NULL  /* <--- Filtro añadido */
                ORDER BY v.fecha_hora_ingreso DESC
                LIMIT 10
            """)
            
            result = await self.db.execute(query, {"user_id": user_id})
            rows = result.fetchall()
            
            return [
                {"categoria": str(row[0]), "duracion_segundos": int(row[1])} 
                for row in rows
            ]
        except Exception as exc:
            raise DatabaseException(f"Error en ML Repository: {exc}")