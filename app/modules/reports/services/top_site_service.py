from typing import List
from app.modules.reports.schemas.top_site_schema import TopSiteResponse
from app.modules.reports.implementation.top_site_repository import TopSiteRepository

class TopSiteService:
    def __init__(self, repo: TopSiteRepository):
        self.repo = repo

    async def get_top_sites(self, user_id: int) -> List[TopSiteResponse]:
        sites = await self.repo.fetch_top_sites(user_id)

        return [
            TopSiteResponse(
                name=site["name"],
                visits=site["visits"],

                time_hours=round(site["total_seconds"] / 3600, 2),
                time_minutes=round(site["total_seconds"] / 60, 2),

                category=None,
                trend=None
            )
            for site in sites
        ]