from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.exceptions import NotFoundException

from app.modules.users.implementation.user_repository import UserRepository
from app.modules.categories.implementation.category_website_repository import CategoryWebsiteRepository
from app.modules.categories.implementation.category_repository import CategoryRepository
from ..implementation.website_repository import WebsiteRepository
from ..implementation.website_user_repository import WebsiteUserRepository

from ..schemas.website_user_schema import (WebsiteUserCreate, WebsiteUserUpdate, WebsiteUserResponse)
from ..services.website_user_service import WebsiteUserService
from ..services.website_service import WebsiteService

router = APIRouter(prefix="/website-users", tags=["website_users"])


def get_service(db: AsyncSession = Depends(get_db)) -> WebsiteUserService:
    website_user_repo = WebsiteUserRepository(db_session=db)
    user_repo = UserRepository(db_session=db)
    website_repo = WebsiteRepository(db_session=db)
    category_repo = CategoryWebsiteRepository(db_session=db)
    category_change_repo = CategoryRepository(db_session=db)
    return WebsiteUserService(
        repo=website_user_repo,
        user_repo=user_repo,
        website_repo=website_repo,
        category_repo=category_repo,
        category_change_repo=category_change_repo
    )


@router.post("/", response_model=WebsiteUserResponse, status_code=status.HTTP_201_CREATED)
async def create_website_user(
    data: WebsiteUserCreate,
    service: WebsiteUserService = Depends(get_service),
) -> WebsiteUserResponse:
    try:
        return await service.create(data)
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc

@router.get("/{website_user_id}", response_model=WebsiteUserResponse)
async def get_user_by_id(
    website_user_id: int,
    service: WebsiteUserService = Depends(get_service),
) -> WebsiteUserResponse:
    return await service.get_by_id(website_user_id)

@router.get("/users/{user_id}", response_model=list[WebsiteUserResponse])
async def get_by_user(
    user_id: int,
    service: WebsiteUserService = Depends(get_service),
) -> list[WebsiteUserResponse]:
    return await service.get_by_user(user_id)


@router.get("/users/{user_id}/sites/{website_id}", response_model=WebsiteUserResponse)
async def get_by_user_and_website(
    user_id: int,
    website_id: int,
    service: WebsiteUserService = Depends(get_service),
) -> WebsiteUserResponse:
    return await service.get_by_user_and_website(user_id, website_id)


@router.get(
    "/users/{user_id}/categories/{category_id}",
    response_model=list[WebsiteUserResponse],
)
async def get_by_user_and_category(
    user_id: int,
    category_id: int,
    service: WebsiteUserService = Depends(get_service),
) -> list[WebsiteUserResponse]:
    return await service.get_by_user_and_category(user_id, category_id)


@router.get("/users/{user_id}/categories/{category_id}/domains", response_model=list[str])
async def get_domains_by_user_and_category(
        user_id: int,
        category_id: int,
    service: WebsiteUserService = Depends(get_service),
) -> list[str]:
    return await service.get_domains_by_user_and_category(user_id, category_id)


@router.put(
    "/users/{user_id}/sites/{website_id}",
    response_model=WebsiteUserResponse,
)
async def update_by_user_and_website(
    user_id: int,
    website_id: int,
    data: WebsiteUserUpdate,
    service: WebsiteUserService = Depends(get_service),
) -> WebsiteUserResponse:
    try:
        return await service.update_by_user_and_website(user_id, website_id, data)
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc

@router.get("/website-with-category/user/{user_id}")       
async def get_website_with_category(
    user_id: int,
    service: WebsiteUserService = Depends(get_service),
):
    try:
        registros = await service.get_user_website_list(user_id)
        return registros
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting website with category: {str(e)}"
        )