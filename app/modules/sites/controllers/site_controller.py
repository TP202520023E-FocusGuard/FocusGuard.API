from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.modules.sites.services.site_service import SiteService
from app.modules.sites.schemas.site_schema import (
    ClassificationBase, NavigationHistoryCreate, NavigationHistoryUpdate,
    CombinedSiteWithClassification, SiteClassificationUpdate, ClassificationResponse
)
from app.core.exceptions import DatabaseException, BusinessException, ValidationException, NotFoundException

router = APIRouter(prefix="/sites", tags=["sites"])

@router.get("/classifications", response_model=List[ClassificationBase])
async def get_classifications(
    db: AsyncSession = Depends(get_db)
):
    """Obtiene todas las clasificaciones disponibles"""
    try:
        service = SiteService(db)
        return await service.get_all_classifications()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting classifications: {str(e)}"
        )


@router.post("/navigation/start")
async def start_navigation_session(
    history_data: NavigationHistoryCreate,
    user_id: int = 1,  # Temporal - luego vendrá del JWT
    db: AsyncSession = Depends(get_db)
):
    """Inicia una sesión de navegación"""
    try:
        service = SiteService(db)
        history_id = await service.start_navigation_session(user_id, history_data)
        return {"history_id": history_id, "message": "Navigation session started"}
    except BusinessException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error starting navigation session: {str(e)}"
        )

@router.put("/navigation/end/{history_id}")
async def end_navigation_session(
    history_id: int,
    update_data: NavigationHistoryUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Finaliza una sesión de navegación y genera predicción ML"""
    try:
        print(f"Iniciando end_navigation_session para history_id: {history_id}")
        
        service = SiteService(db)
        print(f"SiteService creado exitosamente")
        
        success = await service.end_navigation_session(history_id, update_data)
        print(f"end_navigation_session completado: {success}")

        if success:
            print(f"🔍 Llamando a ML Service...")
            from app.modules.ml.services.ml_service import MLService
            ml_service = MLService(db)
            
            prediction = await ml_service.generate_and_store_prediction(user_id=1)
            print(f"🔍 Predicción ML completada: {prediction is not None}")

            response_data = {
                "message": "Navigation session ended successfully"
            }
            
            if prediction:
                response_data["prediction"] = {
                    "focus_level": prediction.focus_level,
                    "needs_intervention": prediction.needs_intervention,
                    "confidence": prediction.confidence,
                    "predicted_duration": prediction.predicted_duration,
                    "risk_factors": prediction.risk_factors
                }
                print(f"Predicción incluida en respuesta")

            return response_data
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Navigation session not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ending navigation session: {str(e)}"
        )
        
@router.get("/user/{user_id}/combined", response_model=List[CombinedSiteWithClassification])
async def get_combined_sites_with_classification(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtiene sitios CURADOS + PERSONALES con clasificaciones"""
    try:
        service = SiteService(db)
        return await service.get_combined_sites_with_classification(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting combined sites: {str(e)}"
        )
    
@router.put("/user/{user_id}/classification", response_model=ClassificationResponse)
async def update_site_classification(
    user_id: int,
    classification_data: SiteClassificationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Actualiza la clasificación de un sitio (base o personal)
    
    - Para sitios base: enviar site_id en el body
    - Para sitios personales: enviar dominio en el body  
    - Siempre enviar id_clasificacion
    """
    try:
        service = SiteService(db)
        return await service.update_site_classification(user_id, classification_data)
    except (ValidationException, NotFoundException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating site classification: {str(e)}"
        )