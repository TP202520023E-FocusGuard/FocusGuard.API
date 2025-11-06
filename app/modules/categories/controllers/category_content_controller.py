#from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from ..implementation.category_content_repository import CategoryContentRepository
from ..schemas.category_content_schema import CategoryContentCreate, CategoryContentResponse
from ..services.category_content_service import CategoryContentService

router = APIRouter(prefix="/categories/content", tags=["categories-content"])


def get_service(db: AsyncSession = Depends(get_db)) -> CategoryContentService:
    repo = CategoryContentRepository(db_session=db)
    return CategoryContentService(repo=repo)


@router.post("/", response_model=CategoryContentResponse, status_code=status.HTTP_201_CREATED)
async def create_category_content(
    data: CategoryContentCreate,
    service: CategoryContentService = Depends(get_service),
):
    try:
        return await service.create_category_content(data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/", response_model=list[CategoryContentResponse])
async def get_all_categories_content(
    service: CategoryContentService = Depends(get_service),
):
    return await service.get_all()


@router.get("/{category_id}", response_model=CategoryContentResponse)
async def get_category_content_by_id(
    category_id: int,
    service: CategoryContentService = Depends(get_service),
):
    try:
        return await service.get_by_id(category_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/nombre/{nombre}", response_model=CategoryContentResponse)
async def get_category_content_by_name(
    nombre: str,
    service: CategoryContentService = Depends(get_service),
):
    try:
        return await service.get_by_name(nombre)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/peso/{peso}", response_model=CategoryContentResponse)
async def get_category_content_by_weight(
    peso: int,
    service: CategoryContentService = Depends(get_service),
):
    try:
        return await service.get_by_weight(peso)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_content_by_id(
    category_id: int,
    service: CategoryContentService = Depends(get_service),
):
    try:
        await service.delete_by_id(category_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc