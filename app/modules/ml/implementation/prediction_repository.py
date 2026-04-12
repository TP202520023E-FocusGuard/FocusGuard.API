from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from app.modules.ml.models.prediction_model import PrediccionSecuencial
from typing import List

class PrediccionFeatureRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_features_by_user(self, user_id: int):
        query = text("""
        SELECT
            c.nombre AS categoria,
            GREATEST(
                TIMESTAMPDIFF(
                    SECOND,
                    v.fecha_hora_ingreso,
                    COALESCE(v.fecha_hora_salida, NOW())
                ),
                1
            ) AS duracion_segundos
        FROM sitios_web_visitados v
        JOIN sitios_web_usuario u ON v.id_sitios_web_usuario = u.id
        JOIN categorias_web c ON u.id_categorias_web = c.id
        WHERE v.id_usuarios = :user_id
          AND v.fecha_hora_salida IS NOT NULL
        ORDER BY v.fecha_hora_ingreso DESC
        LIMIT 10
        """)

        result = await self.session.execute(query, {"user_id": user_id})
        rows = result.fetchall()

        return [
            {
                "categoria": r.categoria,
                "duracion_segundos": float(r.duracion_segundos)
            }
            for r in rows
        ]
    
    async def get_by_user(self, user_id: int) -> List[PrediccionSecuencial]:
        stmt = (
            select(PrediccionSecuencial)
            .where(PrediccionSecuencial.id_usuarios == user_id)
            .order_by(PrediccionSecuencial.ts_prediccion.desc())
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()