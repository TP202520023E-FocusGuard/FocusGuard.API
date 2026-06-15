from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class LeisureTimeRepository:

    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def fetch_leisure_time(
        self, user_id: int, start_date: str, end_date: str
    ):
        """Busca el tiempo real de ocio y distracción de un usuario aplicando

        mitigación de sesiones colgadas (max 2 horas continuas) y fusionando
        solapamientos de pestañas/contenidos en paralelo.

        Parámetros esperados en strings:
        - start_date: '2026-06-08 00:00:00'
        - end_date: '2026-06-14 23:59:59'
        """
        query = text("""
            WITH horas_limpias AS (
                -- 1. Consolidamos sitios web, aplicamos zona horaria y controlamos sesiones colgadas
                SELECT 
                    id_usuarios,
                    CONVERT_TZ(fecha_hora_ingreso, '+00:00', '-05:00') AS ingreso_local,
                    LEAST(
                        CASE 
                            WHEN TIMESTAMPDIFF(SECOND, fecha_hora_ingreso, fecha_hora_salida) > 7200 
                            THEN DATE_ADD(CONVERT_TZ(fecha_hora_ingreso, '+00:00', '-05:00'), INTERVAL 2 HOUR)
                            ELSE CONVERT_TZ(fecha_hora_salida, '+00:00', '-05:00')
                        END, 
                        :end_date
                    ) AS salida_local
                FROM sitios_web_visitados v
                JOIN categorias_web cw ON cw.id = v.id_categorias_web
                WHERE v.id_usuarios = :user_id
                  AND v.fecha_hora_salida IS NOT NULL
                  AND cw.codigo = 'distractivo'
                  AND CONVERT_TZ(v.fecha_hora_ingreso, '+00:00', '-05:00') BETWEEN :start_date AND :end_date
                
                UNION ALL
                
                -- 2. Consolidamos contenidos visitados con las mismas reglas analíticas
                SELECT 
                    cv.id_usuarios,
                    CONVERT_TZ(cv.fecha_hora_ingreso, '+00:00', '-05:00') AS ingreso_local,
                    LEAST(
                        CASE 
                            WHEN TIMESTAMPDIFF(SECOND, cv.fecha_hora_ingreso, cv.fecha_hora_salida) > 7200 
                            THEN DATE_ADD(CONVERT_TZ(cv.fecha_hora_ingreso, '+00:00', '-05:00'), INTERVAL 2 HOUR)
                            ELSE CONVERT_TZ(cv.fecha_hora_salida, '+00:00', '-05:00')
                        END, 
                        :end_date
                    ) AS salida_local
                FROM contenidos_visitados cv
                JOIN contenidos_usuario cu ON cu.id = cv.id_contenidos_usuario
                JOIN categorias_contenido cc ON cc.id = cu.id_categorias_contenido
                WHERE cv.id_usuarios = :user_id
                  AND cv.fecha_hora_salida IS NOT NULL
                  AND cc.es_ocio = 1
                  AND CONVERT_TZ(cv.fecha_hora_ingreso, '+00:00', '-05:00') BETWEEN :start_date AND :end_date
            ),
            intervalos_ordenados AS (
                -- 3. Buscamos el valor máximo de 'salida' registrado hasta el registro inmediato anterior
                SELECT 
                    id_usuarios,
                    ingreso_local,
                    salida_local,
                    MAX(salida_local) OVER (
                        PARTITION BY id_usuarios 
                        ORDER BY ingreso_local, salida_local 
                        ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
                    ) AS max_salida_anterior
                FROM horas_limpias
            ),
            intervalos_fusionados AS (
                -- 4. Evaluamos si hay solapamiento de pestañas para no duplicar minutos reales de reloj
                SELECT 
                    WEEKDAY(ingreso_local) AS weekday,
                    DAYNAME(ingreso_local) AS day,
                    CASE 
                        WHEN max_salida_anterior >= salida_local THEN 0
                        WHEN max_salida_anterior > ingreso_local THEN TIMESTAMPDIFF(SECOND, max_salida_anterior, salida_local) / 3600
                        ELSE TIMESTAMPDIFF(SECOND, ingreso_local, salida_local) / 3600
                    END AS horas_reales
                FROM intervalos_ordenados
            )
            -- 5. Agrupación final por número y nombre de día de la semana
            SELECT 
                weekday,
                day,
                ROUND(SUM(horas_reales), 2) AS total_hours
            FROM intervalos_fusionados
            GROUP BY weekday, day
            ORDER BY weekday;
        """)

        result = await self.session.execute(
            query,
            {
                "user_id": user_id,
                "start_date": start_date,
                "end_date": end_date,
            },
        )

        return result.mappings().all()
