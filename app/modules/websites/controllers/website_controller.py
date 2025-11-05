from fastapi import APIRouter, Depends, HTTPException, status

#from sqlalchemy.orm import Session
#from ....database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

from ..schemas.website_schema import WebsiteCreate, WebsiteResponse
from ..services.website_service import WebsiteService
from ..implementation.website_repository import WebsiteRepository

router = APIRouter(prefix="/websites", tags=["websites"])


def get_service(db: AsyncSession = Depends(get_db)) -> WebsiteService:
    repo = WebsiteRepository(db_session=db)
    return WebsiteService(repo=repo)


@router.post("/", response_model=WebsiteResponse, status_code=status.HTTP_201_CREATED)
async def crear_website(
        data: WebsiteCreate,
        service: WebsiteService = Depends(get_service)
):
    try:
        nuevo_website = await service.crear_website(data)
        return nuevo_website

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))