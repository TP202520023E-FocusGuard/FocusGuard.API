from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import pytz


class LeisureTimeRepository:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    def _to_utc(self, dt: datetime):
        """Convierte hora de Perú (o naive) a UTC"""
        lima = pytz.timezone("America/Lima")

        if dt.tzinfo is None:
            dt = lima.localize(dt)

        return dt.astimezone(pytz.UTC)

    async def fetch_leisure_time(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime
    ):
        start_date = self._to_utc(start_date)
        end_date = self._to_utc(end_date)

        query = text("""
            SELECT
                weekday,
                day,
                ROUND(SUM(hours), 2) AS total_hours
            FROM (
                SELECT
                    WEEKDAY(CONVERT_TZ(v.fecha_hora_ingreso, '+00:00', '-05:00')) AS weekday,
                    DAYNAME(CONVERT_TZ(v.fecha_hora_ingreso, '+00:00', '-05:00')) AS day,
                    TIMESTAMPDIFF(
                        SECOND,
                        v.fecha_hora_ingreso,
                        v.fecha_hora_salida
                    ) / 3600 AS hours
                FROM sitios_web_visitados v
                JOIN categorias_web cw
                    ON cw.id = v.id_categorias_web
                WHERE v.id_usuarios = :user_id
                    AND v.fecha_hora_salida IS NOT NULL
                    AND cw.codigo = 'distractivo'
                    AND v.fecha_hora_ingreso BETWEEN :start_date AND :end_date

                UNION ALL

                SELECT
                    WEEKDAY(CONVERT_TZ(cv.fecha_hora_ingreso, '+00:00', '-05:00')) AS weekday,
                    DAYNAME(CONVERT_TZ(cv.fecha_hora_ingreso, '+00:00', '-05:00')) AS day,
                    TIMESTAMPDIFF(
                        SECOND,
                        cv.fecha_hora_ingreso,
                        cv.fecha_hora_salida
                    ) / 3600 AS hours
                FROM contenidos_visitados cv
                JOIN contenidos_usuario cu
                    ON cu.id = cv.id_contenidos_usuario
                JOIN categorias_contenido cc
                    ON cc.id = cu.id_categorias_contenido
                WHERE cv.id_usuarios = :user_id
                    AND cv.fecha_hora_salida IS NOT NULL
                    AND cc.es_ocio = 1
                    AND cv.fecha_hora_ingreso BETWEEN :start_date AND :end_date
            ) AS combined
            GROUP BY weekday, day
            ORDER BY weekday;
        """)

        result = await self.session.execute(
            query,
            {
                "user_id": user_id,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        return result.mappings().all()