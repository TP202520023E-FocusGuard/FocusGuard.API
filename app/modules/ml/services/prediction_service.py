from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
import httpx
import hashlib
import json

from app.modules.ml.models.prediction_model import PrediccionSecuencial
from app.modules.ml.schemas.prediction_schema import PrediccionRequest
from app.modules.ml.implementation.prediction_repository import PrediccionFeatureRepository
from app.core.exceptions import DatabaseException


class PredictionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = PrediccionFeatureRepository(session)

        self.ml_url = "https://focusguard-ml-api-c4d2cuarh3byeadf.eastus-01.azurewebsites.net/decision"

        self.model_version = "modelo_procrastinacion_v1"

    async def generate_prediction(self, request: PrediccionRequest):
        try:
            # =====================================================
            # 1. FEATURES
            # =====================================================
            features = await self.repo.get_features_by_user(request.id_usuarios)

            payload = {
                "id_usuario": request.id_usuarios,
                "registros": features,

                # opcional: puedes enriquecer estado DQN
                "intervenciones_recientes": 0.0,
                "ocio": 0.5
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.ml_url,
                    json=payload,
                    timeout=20.0
                )

            response.raise_for_status()
            ml_result = response.json()

            features_hash = self._generate_hash(payload)

            prediction = PrediccionSecuencial(
                id_usuarios=request.id_usuarios,
                ts_prediccion=datetime.now(timezone.utc),

                horizonte_segundos=ml_result.get("horizon_seconds", 7200),
                prob_procrastinacion=ml_result.get("score", 0.0),
                umbral_decision=ml_result.get("umbral_decision", 0.5),
                is_procrastinating=ml_result.get("is_procrastinating", False),

                version_modelo=ml_result.get("model_version", self.model_version),

                features_hash=features_hash
            )

            self.session.add(prediction)
            await self.session.commit()
            await self.session.refresh(prediction)

            return {
                # --- BD DATA ---
                "id": prediction.id,
                "id_usuarios": prediction.id_usuarios,

                "prob_procrastinacion": prediction.prob_procrastinacion,
                "is_procrastinating": prediction.is_procrastinating,

                "umbral_decision": prediction.umbral_decision,
                "version_modelo": prediction.version_modelo,
                "horizonte_segundos": prediction.horizonte_segundos,
                "ts_prediccion": prediction.ts_prediccion,

                # --- DQN DATA (runtime only) ---
                "action": ml_result.get("action"),
                "source": ml_result.get("source") or "fallback",
                "raw_action": ml_result.get("raw_action"),
                "q_values": ml_result.get("q_values")
            }

        except httpx.RequestError as e:
            await self.session.rollback()
            raise DatabaseException(f"Error conectando con ML service: {str(e)}")

        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(f"Error en predicción: {str(e)}")

    def _generate_hash(self, payload: dict) -> str:
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()

    async def get_predictions_by_user(self, user_id: int):
        try:
            return await self.repo.get_by_user(user_id)

        except Exception as e:
            raise DatabaseException(f"Error obteniendo predicciones: {str(e)}")
