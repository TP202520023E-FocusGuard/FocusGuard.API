from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import NotFoundException

from app.modules.users.implementation.user_repository import UserRepository
from ..implementation.content_user_repository import ContentUserRepository
from ..implementation.content_visited_repository import ContentVisitedRepository

from ..schemas.content_visited_schema import ContentVisitedCreate, ContentVisitedResponse
from ..services.content_visited_service import ContentVisitedService

router = APIRouter(prefix="/content-visited", tags=["content_visited"])


def get_service(db: AsyncSession = Depends(get_db)) -> ContentVisitedService:
    repo = ContentVisitedRepository(db_session=db)
    user_repo = UserRepository(db_session=db)
    content_user_repo = ContentUserRepository(db_session=db)
    return ContentVisitedService(
        repo=repo,
        user_repo=user_repo,
        content_user_repo=content_user_repo,
    )


@router.post("/", response_model=ContentVisitedResponse, status_code=status.HTTP_201_CREATED)
async def create_content_visited(
    data: ContentVisitedCreate,
    service: ContentVisitedService = Depends(get_service),
) -> ContentVisitedResponse:
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


@router.get("/", response_model=list[ContentVisitedResponse])
async def get_all_content_visited(
    service: ContentVisitedService = Depends(get_service),
) -> list[ContentVisitedResponse]:
    return await service.get_all()


@router.get("/{record_id}", response_model=ContentVisitedResponse)
async def get_content_visited_by_id(
    record_id: int,
    service: ContentVisitedService = Depends(get_service),
) -> ContentVisitedResponse:
    try:
        return await service.get_by_id(record_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get("/user/{user_id}", response_model=list[ContentVisitedResponse])
async def get_content_visited_by_user(
    user_id: int,
    service: ContentVisitedService = Depends(get_service),
) -> list[ContentVisitedResponse]:
    return await service.get_by_user(user_id)


@router.get(
    "/user/{user_id}/content-user/{content_user_id}",
    response_model=list[ContentVisitedResponse],
)
async def get_content_visited_by_user_and_content_user(
    user_id: int,
    content_user_id: int,
    service: ContentVisitedService = Depends(get_service),
) -> list[ContentVisitedResponse]:
    return await service.get_by_user_and_content_user(user_id, content_user_id)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content_visited(
    record_id: int,
    service: ContentVisitedService = Depends(get_service),
) -> None:
    try:
        await service.delete_by_id(record_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc