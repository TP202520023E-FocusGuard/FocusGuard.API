from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.exceptions import NotFoundException

from app.modules.users.implementation.user_repository import UserRepository
from ..implementation.website_user_repository import WebsiteUserRepository
from ..implementation.website_visited_repository import WebsiteVisitedRepository

from ..schemas.website_visited_schema import WebsiteVisitedCreate, WebsiteVisitedResponse
from ..services.website_visited_service import WebsiteVisitedService

router = APIRouter(prefix="/website-visited", tags=["website_visited"])


def get_service(db: AsyncSession = Depends(get_db)) -> WebsiteVisitedService:
    repo = WebsiteVisitedRepository(db_session=db)
    user_repo = UserRepository(db_session=db)
    website_user_repo = WebsiteUserRepository(db_session=db)
    return WebsiteVisitedService(
        repo=repo,
        user_repo=user_repo,
        website_user_repo=website_user_repo,
    )


@router.post("/", response_model=WebsiteVisitedResponse, status_code=status.HTTP_201_CREATED)
async def create_visit(
    data: WebsiteVisitedCreate,
    service: WebsiteVisitedService = Depends(get_service),
) -> WebsiteVisitedResponse:
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


@router.get("/{visit_id}", response_model=WebsiteVisitedResponse)
async def get_visit_by_id(
    visit_id: int,
    service: WebsiteVisitedService = Depends(get_service),
) -> WebsiteVisitedResponse:
    try:
        return await service.get_by_id(visit_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get("/users/{user_id}", response_model=list[WebsiteVisitedResponse])
async def get_visits_by_user(
    user_id: int,
    service: WebsiteVisitedService = Depends(get_service),
) -> list[WebsiteVisitedResponse]:
    return await service.get_by_user(user_id)


@router.get(
    "/users/{user_id}/interval",
    response_model=list[WebsiteVisitedResponse],
)
async def get_visits_by_user_and_interval(
    user_id: int,
    start: datetime = Query(..., description="Fecha y hora de inicio del intervalo"),
    end: datetime = Query(..., description="Fecha y hora de fin del intervalo"),
    service: WebsiteVisitedService = Depends(get_service),
) -> list[WebsiteVisitedResponse]:
    try:
        return await service.get_by_user_and_interval(user_id, start, end)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.delete("/{visit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_visit(
    visit_id: int,
    service: WebsiteVisitedService = Depends(get_service),
) -> None:
    try:
        await service.delete_by_id(visit_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc