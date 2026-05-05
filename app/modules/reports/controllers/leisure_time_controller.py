from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.modules.reports.schemas.leisure_time_schema import LeisureTimeResponse
from app.modules.reports.implementation.leisure_time_repository import LeisureTimeRepository
from app.modules.reports.services.leisure_time_service import LeisureTimeService


router = APIRouter(
    prefix="/reports/weekly-leisure-hours",
    tags=["leisure_time"]
)


async def get_service(db: AsyncSession = Depends(get_db)) -> LeisureTimeService:
    repo = LeisureTimeRepository(db_session=db)
    return LeisureTimeService(repo=repo)


@router.get("/", response_model=List[LeisureTimeResponse])
async def get_leisure_time(
    user_id: int,

    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),

    service: LeisureTimeService = Depends(get_service)
):
    """
    Obtiene el tiempo de ocio acumulado por día dentro de un rango de fechas.
    """

    try:
        return await service.get_leisure_time(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )