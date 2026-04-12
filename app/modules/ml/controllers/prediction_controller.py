from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.modules.ml.services.prediction_service import PredictionService
from app.modules.ml.schemas.prediction_schema import PrediccionRequest, PrediccionResponse


router = APIRouter(prefix="/ml", tags=["Machine Learning"])


def get_service(db: AsyncSession = Depends(get_db)) -> PredictionService:
    return PredictionService(db)


@router.post("/predict", response_model=PrediccionResponse)
async def generate_prediction(
    request: PrediccionRequest,
    service: PredictionService = Depends(get_service)
):
    try:
        return await service.generate_prediction(request)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/predictions/{user_id}", response_model=List[PrediccionResponse])
async def get_predictions_by_user(
    user_id: int,
    service: PredictionService = Depends(get_service)
):
    try:
        return await service.get_predictions_by_user(user_id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )