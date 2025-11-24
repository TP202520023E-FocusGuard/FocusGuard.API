from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.modules.categories.services.category_service import ChangeCategoryService
from app.modules.categories.schemas.category_schema import (
    ChangeCategory, ChangeCategoryCreate
)
from app.modules.users.implementation.user_repository import UserRepository
from app.modules.websites.implementation.website_repository import WebsiteRepository
from app.modules.websites.implementation.website_user_repository import WebsiteUserRepository
from app.modules.categories.implementation.category_website_repository import CategoryWebsiteRepository
from app.modules.websites.services.website_user_service import WebsiteUserService

from app.modules.categories.implementation.category_repository import CategoryRepository

router = APIRouter(prefix="/change-category", tags=["change_category"])

async def get_service(db: AsyncSession = Depends(get_db)) -> ChangeCategoryService:
    repo = CategoryRepository(db_session=db)
    user_repo = UserRepository(db_session=db)
    website_repo = WebsiteRepository(db_session=db)
    website_user_repo = WebsiteUserRepository(db_session=db)
    category_repo = CategoryWebsiteRepository(db_session=db)

    # Servicio de websites de usuario
    website_user_service = WebsiteUserService(
        repo=website_user_repo,
        user_repo=user_repo,
        website_repo=website_repo,
        category_repo=category_repo
    )

    # Servicio de cambios de categoría
    return ChangeCategoryService(
        repo=repo,
        website_user_service=website_user_service
    )

@router.get("/", response_model=List[ChangeCategory])
async def get_all_changes(service: ChangeCategoryService = Depends(get_service)):
    """
    Obtiene todos los cambios de categoría.
    """
    return await service.get_all()


@router.get("/{change_id}", response_model=ChangeCategory)
async def get_change_by_id(change_id: int, service: ChangeCategoryService = Depends(get_service)):
    """
    Obtiene un cambio de categoría por ID.
    """
    try:
        return await service.get_by_id(change_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=ChangeCategory)
async def create_change(data: ChangeCategoryCreate, service: ChangeCategoryService = Depends(get_service)):
    """
    Crea un nuevo registro de cambio de categoría.
    """
    return await service.create(data)
