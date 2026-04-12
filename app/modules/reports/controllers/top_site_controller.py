from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db

from app.modules.reports.schemas.top_site_schema import TopSiteResponse
from app.modules.reports.implementation.top_site_repository import TopSiteRepository
from app.modules.reports.services.top_site_service import TopSiteService

router = APIRouter(prefix="/reports/top-sites", tags=["top_sites"])

async def get_service(db: AsyncSession = Depends(get_db)) -> TopSiteService:
    repo = TopSiteRepository(db_session=db)
    return TopSiteService(repo=repo)

@router.get("/", response_model=List[TopSiteResponse])
async def get_top_sites(
    user_id: int,
    service: TopSiteService = Depends(get_service)
):
    """
    Obtiene los top 5 sitios más visitados por usuario,
    ordenados por tiempo total de uso (procrastinación real).
    """
    try:
        return await service.get_top_sites(user_id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )