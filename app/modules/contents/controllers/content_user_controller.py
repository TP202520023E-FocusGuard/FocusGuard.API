from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import NotFoundException

from app.modules.users.implementation.user_repository import UserRepository
from app.modules.websites.implementation.website_user_repository import WebsiteUserRepository
from app.modules.categories.implementation.category_content_repository import CategoryContentRepository
from ..implementation.content_repository import ContentRepository
from ..implementation.content_user_repository import ContentUserRepository

from ..schemas.content_user_schema import ContentUserCreate, ContentUserUpdate, ContentUserResponse
from ..services.content_user_service import ContentUserService

router = APIRouter(prefix="/content-users", tags=["content-users"])


def get_service(db: AsyncSession = Depends(get_db)) -> ContentUserService:
    repo = ContentUserRepository(db_session=db)
    user_repo = UserRepository(db_session=db)
    content_repo = ContentRepository(db_session=db)
    category_content_repo = CategoryContentRepository(db_session=db)
    website_user_repo = WebsiteUserRepository(db_session=db)
    return ContentUserService(
        repo=repo,
        user_repo=user_repo,
        content_repo=content_repo,
        category_content_repo=category_content_repo,
        website_user_repo=website_user_repo
    )


@router.post("/", response_model=ContentUserResponse, status_code=status.HTTP_201_CREATED)
async def create_content_user(
    data: ContentUserCreate,
    service: ContentUserService = Depends(get_service),
) -> ContentUserResponse:
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


@router.get("/", response_model=list[ContentUserResponse])
async def get_all_content_users(
    service: ContentUserService = Depends(get_service),
) -> list[ContentUserResponse]:
    return await service.get_all()


@router.get("/{record_id}", response_model=ContentUserResponse)
async def get_content_user_by_id(
    record_id: int,
    service: ContentUserService = Depends(get_service),
) -> ContentUserResponse:
    try:
        return await service.get_by_id(record_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get("/user/{user_id}", response_model=list[ContentUserResponse])
async def get_content_users_by_user(
    user_id: int,
    service: ContentUserService = Depends(get_service),
) -> list[ContentUserResponse]:
    return await service.get_by_user(user_id)


@router.get(
    "/user/{user_id}/site/{site_id}", response_model=list[ContentUserResponse]
)
async def get_content_users_by_user_and_site(
    user_id: int,
    site_id: int,
    service: ContentUserService = Depends(get_service),
) -> list[ContentUserResponse]:
    return await service.get_by_user_and_site(user_id, site_id)


# @router.get(
#     "/user/{user_id}/site/{site_id}/content/{content_id}",
#     response_model=list[ContentUserResponse],
# )
# async def get_content_users_by_user_site_and_content(
#     user_id: int,
#     site_id: int,
#     content_id: int,
#     service: ContentUserService = Depends(get_service),
# ) -> list[ContentUserResponse]:
#     return await service.get_by_user_site_and_content(user_id, site_id, content_id)

@router.get(
    "/user/{user_id}/site/{site_id}/content/{content_id}",
    response_model=ContentUserResponse,
)
async def get_content_users_by_user_site_and_content(
    user_id: int,
    site_id: int,
    content_id: int,
    service: ContentUserService = Depends(get_service),
) -> ContentUserResponse:
    return await service.get_by_user_site_and_content(user_id, site_id, content_id)


@router.get(
    "/user/{user_id}/category/{category_id}",
    response_model=list[ContentUserResponse],
)
async def get_content_users_by_user_and_category(
    user_id: int,
    category_id: int,
    service: ContentUserService = Depends(get_service),
) -> list[ContentUserResponse]:
    return await service.get_by_user_and_category(user_id, category_id)

@router.put(
    "/user/{content_user_id}",
    response_model=ContentUserResponse,
)
async def update_by_id(
    content_user_id: int,
    data: ContentUserUpdate,
    service: ContentUserService = Depends(get_service),
) -> ContentUserResponse:
    try:
        return await service.update_by_id(content_user_id, data)
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content_user(
    record_id: int,
    service: ContentUserService = Depends(get_service),
) -> None:
    try:
        await service.delete_by_id(record_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc