from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from ..implementation.content_repository import ContentRepository
from ..schemas.content_schema import ContentCreate, ContentResponse
from ..services.content_service import ContentService

router = APIRouter(prefix="/contents", tags=["contents"])


def get_service(db: AsyncSession = Depends(get_db)) -> ContentService:
    repo = ContentRepository(db_session=db)
    return ContentService(repo=repo)


@router.post("/", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def create_content(
    data: ContentCreate,
    service: ContentService = Depends(get_service),
) -> ContentResponse:
    try:
        return await service.create_content(data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/", response_model=list[ContentResponse])
async def get_all_contents(
    service: ContentService = Depends(get_service),
) -> list[ContentResponse]:
    return await service.get_contents()


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content_by_id(
    content_id: int,
    service: ContentService = Depends(get_service),
) -> ContentResponse:
    try:
        return await service.get_by_id(content_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content_by_id(
    content_id: int,
    service: ContentService = Depends(get_service),
) -> None:
    try:
        await service.delete_by_id(content_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc