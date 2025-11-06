from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from ..schemas.category_website_schema import CategoryWebsiteCreate, CategoryWebsiteResponse
from ..services.category_website_service import CategoryWebsiteService
from ..implementation.category_website_repository import CategoryWebsiteRepository

router = APIRouter(prefix="/categories/web", tags=["categories-web"])


def get_service(db: AsyncSession = Depends(get_db)) -> CategoryWebsiteService:
    repo = CategoryWebsiteRepository(db_session=db)
    return CategoryWebsiteService(repo=repo)


@router.post("/", response_model=CategoryWebsiteResponse, status_code=status.HTTP_201_CREATED)
async def create_category_website(
    data: CategoryWebsiteCreate,
    service: CategoryWebsiteService = Depends(get_service),
):
    try:
        return await service.create_category_website(data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{category_id}", response_model=CategoryWebsiteResponse)
async def get_category_by_id(
    category_id: int,
    service: CategoryWebsiteService = Depends(get_service),
):
    try:
        return await service.get_by_id(category_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/nombre/{nombre}", response_model=CategoryWebsiteResponse)
async def get_category_by_name(
    nombre: str,
    service: CategoryWebsiteService = Depends(get_service),
):
    try:
        return await service.get_by_name(nombre)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/peso/{peso}", response_model=CategoryWebsiteResponse)
async def get_category_by_weight(
    peso: int,
    service: CategoryWebsiteService = Depends(get_service),
):
    try:
        return await service.get_by_weight(peso)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_by_id(
    category_id: int,
    service: CategoryWebsiteService = Depends(get_service),
):
    try:
        await service.delete_by_id(category_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc