from fastapi import APIRouter, HTTPException, status

from ..schemas.ml_prediction_schema import ModelClassificationInput, ModelClassificationOutput
from ..predictions import cargar_modelo_clasificacion, obtener_predicciones

router = APIRouter(prefix="/ml_classification", tags=["ml_classification"])
modelo_pipe = cargar_modelo_clasificacion()

@router.post("/", response_model=ModelClassificationOutput, status_code=status.HTTP_201_CREATED)
async def predict_content(
        data: ModelClassificationInput
) -> ModelClassificationOutput:
    try:
        prediccion, probabilidades = obtener_predicciones(modelo_pipe, data.texto)
        clases = ['No ocio', 'Ocio']

        return ModelClassificationOutput(probabilidad_no_ocio=probabilidades[0],
                                         probabilidad_ocio=probabilidades[1],
                                         etiqueta_predicha=clases[prediccion])
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
