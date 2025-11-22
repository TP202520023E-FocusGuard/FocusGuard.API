from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from ..schemas.prediction_schema import (
    SequenceRequest,
    SequencePrediction,
    PredictionCreate,
    PredictionResponse,
)
from ..services.prediction_service import PredictionService
from ..services.ml_service import MLService

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

ml_service = MLService()
prediction_service = PredictionService()


@router.post("/predict-sequence", response_model=PredictionResponse)
async def predict_sequence(
    request: SequenceRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint principal que:
      1. Recibe la secuencia de navegación.
      2. Llama al servicio ML para obtener la predicción.
      3. Guarda la predicción y su relación con los historiales.
      4. Devuelve el resultado al frontend.
    """

    try:
        ml_result: SequencePrediction = await ml_service.predict_sequence(request)

        new_prediction = PredictionCreate(
            user_id=request.user_id,
            model_name="sequence_intervention",
            input_data=request.dict(),
            output_data=ml_result.dict(),
            historiales_ids=[h.id_historial for h in request.navigation_sessions]
        )

        created_prediction = await prediction_service.create_prediction(db, new_prediction)

        return created_prediction

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictions/{user_id}", response_model=List[PredictionResponse])
async def get_user_predictions(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    🔹 Devuelve todas las predicciones realizadas para un usuario,
       ordenadas por fecha de creación.
    """
    try:
        predictions = await prediction_service.get_predictions_by_user(db, user_id)
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
