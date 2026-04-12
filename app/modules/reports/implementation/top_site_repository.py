from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

class TopSiteRepository:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def fetch_top_sites(self, user_id: int):

        query = text("""
            SELECT 
                sw.dominio AS name,
                COUNT(swv.id) AS visits,
                COALESCE(
                    SUM(
                        TIMESTAMPDIFF(
                            SECOND, 
                            swv.fecha_hora_ingreso, 
                            swv.fecha_hora_salida
                        )
                    ),
                    0
                ) AS total_seconds
            FROM sitios_web_visitados swv
            JOIN sitios_web_usuario swu 
                ON swv.id_sitios_web_usuario = swu.id
            JOIN sitios_web sw 
                ON swu.id_sitios_web = sw.id
            WHERE swv.id_usuarios = :user_id
            GROUP BY sw.dominio
            ORDER BY total_seconds DESC
            LIMIT 5;
        """)

        result = await self.session.execute(query, {"user_id": user_id})

        rows = result.mappings().all()

        return rows