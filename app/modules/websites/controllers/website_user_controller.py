from fastapi import APIRouter, Depends, HTTPException, status

#from sqlalchemy.orm import Session
#from ....database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

from ..implementation.website_user_repository import WebsiteUserRepository
from ..schemas.website_user_schema import (WebsiteUserCreate, WebsiteUserUpdate, WebsiteUserResponse)
from ..services.website_user_service import WebsiteUserService

router = APIRouter(prefix="/website-users", tags=["website_users"])


def get_service(db: AsyncSession = Depends(get_db)) -> WebsiteUserService:
    repo = WebsiteUserRepository(db_session=db)
    return WebsiteUserService(repo=repo)


@router.post("/", response_model=WebsiteUserResponse, status_code=status.HTTP_201_CREATED)
def create_website_user(
    data: WebsiteUserCreate,
    service: WebsiteUserService = Depends(get_service),
) -> WebsiteUserResponse:
    try:
        return service.create(data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/users/{user_id}", response_model=list[WebsiteUserResponse])
def get_by_user(
    user_id: int,
    service: WebsiteUserService = Depends(get_service),
) -> list[WebsiteUserResponse]:
    return service.get_by_user(user_id)


@router.get("/users/{user_id}/sites/{website_id}", response_model=WebsiteUserResponse)
def get_by_user_and_website(
    user_id: int,
    website_id: int,
    service: WebsiteUserService = Depends(get_service),
) -> WebsiteUserResponse:
    return service.get_by_user_and_website(user_id, website_id)


@router.get(
    "/users/{user_id}/categories/{category_id}",
    response_model=list[WebsiteUserResponse],
)
def get_by_user_and_category(
    user_id: int,
    category_id: int,
    service: WebsiteUserService = Depends(get_service),
) -> list[WebsiteUserResponse]:
    return service.get_by_user_and_category(user_id, category_id)


@router.put(
    "/users/{user_id}/sites/{website_id}",
    response_model=WebsiteUserResponse,
)
def update_by_user_and_website(
    user_id: int,
    website_id: int,
    data: WebsiteUserUpdate,
    service: WebsiteUserService = Depends(get_service),
) -> WebsiteUserResponse:
    try:
        return service.update_by_user_and_website(user_id, website_id, data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc