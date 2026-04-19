from typing import List
from app.modules.reports.schemas.leisure_time_schema import LeisureTimeResponse
from app.modules.reports.implementation.leisure_time_repository import LeisureTimeRepository


class LeisureTimeService:
    def __init__(self, repo: LeisureTimeRepository):
        self.repo = repo

    async def get_leisure_time(
        self,
        user_id: int,
        start_date,
        end_date
    ) -> List[LeisureTimeResponse]:

        # 1. Obtener datos filtrados por rango de fechas
        leisure_data = await self.repo.fetch_leisure_time(
            user_id,
            start_date,
            end_date
        )

        # 2. Transformación ligera (DTO mapping)
        return [
            LeisureTimeResponse(
                weekday=entry["weekday"],
                day=entry["day"],
                total_hours=round(entry["total_hours"], 2)
            )
            for entry in leisure_data
        ]