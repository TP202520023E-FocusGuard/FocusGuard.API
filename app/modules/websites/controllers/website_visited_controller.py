from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ....database import get_db
from ..implementation.website_visited_repository import WebsiteVisitedRepository
from ..schemas.website_visited_schema import WebsiteVisitedCreate, WebsiteVisitedResponse
from ..services.website_visited_service import WebsiteVisitedService

router = APIRouter(prefix="/website-visited", tags=["website_visited"])


def get_service(db: Session = Depends(get_db)) -> WebsiteVisitedService:
    repo = WebsiteVisitedRepository(db_session=db)
    return WebsiteVisitedService(repo=repo)


@router.post("/", response_model=WebsiteVisitedResponse, status_code=status.HTTP_201_CREATED)
def create_visit(
    data: WebsiteVisitedCreate,
    service: WebsiteVisitedService = Depends(get_service),
) -> WebsiteVisitedResponse:
    try:
        return service.create(data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/{visit_id}", response_model=WebsiteVisitedResponse)
def get_visit_by_id(
    visit_id: int,
    service: WebsiteVisitedService = Depends(get_service),
) -> WebsiteVisitedResponse:
    try:
        return service.get_by_id(visit_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get("/users/{user_id}", response_model=list[WebsiteVisitedResponse])
def get_visits_by_user(
    user_id: int,
    service: WebsiteVisitedService = Depends(get_service),
) -> list[WebsiteVisitedResponse]:
    return service.get_by_user(user_id)


@router.get(
    "/users/{user_id}/interval",
    response_model=list[WebsiteVisitedResponse],
)
def get_visits_by_user_and_interval(
    user_id: int,
    start: datetime = Query(..., description="Fecha y hora de inicio del intervalo"),
    end: datetime = Query(..., description="Fecha y hora de fin del intervalo"),
    service: WebsiteVisitedService = Depends(get_service),
) -> list[WebsiteVisitedResponse]:
    try:
        return service.get_by_user_and_interval(user_id, start, end)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.delete("/{visit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_visit(
    visit_id: int,
    service: WebsiteVisitedService = Depends(get_service),
) -> None:
    try:
        service.delete_by_id(visit_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc