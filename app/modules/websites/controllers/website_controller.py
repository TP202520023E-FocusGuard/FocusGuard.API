from fastapi import APIRouter, Depends, HTTPException, status

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
async def create_website(
        data: WebsiteCreate,
        service: WebsiteService = Depends(get_service),
) -> WebsiteResponse:
    try:
        return await service.create_website(data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc

@router.get("/", response_model=list[WebsiteResponse])
async def get_all_websites(
    service: WebsiteService = Depends(get_service),
) -> list[WebsiteResponse]:
    return await service.get_websites()

@router.get("/{website_id}", response_model=WebsiteResponse)
async def get_website_by_id(
    website_id: int,
    service: WebsiteService = Depends(get_service),
) -> WebsiteResponse:
    try:
        return await service.get_by_id(website_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc

@router.get("/by-domain/{dominio}", response_model=WebsiteResponse)
async def gey_website_by_domain(
    dominio: str,
    service: WebsiteService = Depends(get_service),
) -> WebsiteResponse:
    try:
        return await service.get_by_domain(dominio)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete("/{website_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_website_by_id(
    website_id: int,
    service: WebsiteService = Depends(get_service),
) -> None:
    try:
        await service.delete_by_id(website_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete("/by-domain/{dominio}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_website_by_domain(
    dominio: str,
    service: WebsiteService = Depends(get_service),
) -> None:
    try:
        await service.delete_by_domain(dominio)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc