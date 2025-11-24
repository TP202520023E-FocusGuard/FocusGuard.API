from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import httpx
import json

from app.modules.sites.models.site_model import NavigationHistoryModel
from app.modules.ml.models.prediction_model import MLPredictionLog, PrediccionHistorial
from app.core.exceptions import DatabaseException

class PredictionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.ml_url = "http://localhost:8000/api/v1/sequential/predict"

    async def generate_and_store_prediction(self, user_id: int):
        """
        Genera una predicción basada en los últimos 10 historiales del usuario
        """
        try:
            print(f"🔍 Iniciando predicción para usuario {user_id}")
            
            result = await self.session.execute(
                select(NavigationHistoryModel)
                .where(NavigationHistoryModel.id_usuario == user_id)
                .order_by(NavigationHistoryModel.fecha_inicio.desc())
                .limit(10)
            )
            histories = result.scalars().all()
            
            if not histories:
                print("⚠️ No hay historiales para generar predicción")
                return None

            print(f"📊 Encontrados {len(histories)} historiales")

            historial = []
            historiales_ids = []
            
            for h in histories:
                session_data = {
                    "dominio": h.dominio,
                    "fecha_inicio": h.fecha_inicio.isoformat(),
                    "fecha_fin": h.fecha_fin.isoformat() if h.fecha_fin else h.fecha_inicio.isoformat(),  # Usar fecha_inicio si fin es None
                    "duracion_segundos": int(h.duracion_segundos) if h.duracion_segundos else 0,
                    "dia_semana": h.dia_semana.value if hasattr(h.dia_semana, 'value') else str(h.dia_semana),
                    "hora_dia": self._convert_hora_dia_to_int(h.hora_dia),  # Convertir a número
                    "es_fin_semana": bool(h.es_fin_semana),
                    "patron_uso": h.patron_uso.value if hasattr(h.patron_uso, 'value') else str(h.patron_uso),
                    "contexto_anterior": h.contexto_anterior or "navegacion",
                    "fue_bloqueado": bool(h.fue_bloqueado),
                    "usuario_ignoro_advertencia": bool(h.usuario_ignoro_advertencia)
                }
                
                historial.append(session_data)
                historiales_ids.append(h.id_historial)

            payload = {
                "id_usuario": user_id,  # ❗Entero, no string
                "historial": historial  # ❗Se llama "historial", no "navigation_sessions"
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.ml_url, 
                    json=payload, 
                    timeout=30.0
                )

                if response.status_code != 200:
                    error_detail = response.text
                    print(f"Error {response.status_code} from ML: {error_detail}")
                    try:
                        error_json = response.json()
                        print(f"Error details: {error_json}")
                    except:
                        pass
                    response.raise_for_status()
                    
                prediction_data = response.json()

            prediction = MLPredictionLog(
                user_id=str(user_id),  # Guardar como string en BD
                modelo_tipo="secuencial",
                focus_level=prediction_data.get("focus_level"),
                needs_intervention=prediction_data.get("needs_intervention", False),
                confidence=prediction_data.get("confidence"),
                predicted_duration=prediction_data.get("predicted_duration"),
                risk_factors=prediction_data.get("risk_factors", []),
                sequence_stats=prediction_data.get("sequence_stats", {}),
                fecha_prediccion=datetime.now(),
                ejecutado_por="sistema",
                observaciones=f"Predicción generada automáticamente para {len(histories)} historiales"
            )
            
            self.session.add(prediction)
            await self.session.flush()

            for historial_id in historiales_ids:
                relation = PrediccionHistorial(
                    id_prediccion=prediction.id_prediccion,
                    id_historial=historial_id
                )
                self.session.add(relation)

            await self.session.commit()
            
            print(f"💾 Predicción {prediction.id_prediccion} guardada exitosamente")
            return prediction

        except httpx.RequestError as e:
            await self.session.rollback()
            print(f"Error de conexión con ML: {str(e)}")
            raise DatabaseException(f"Error conectando con el servicio ML: {str(e)}")
        except Exception as e:
            await self.session.rollback()
            print(f"Error generando predicción: {str(e)}")
            raise DatabaseException(f"Error generating prediction: {str(e)}")

    def _convert_hora_dia_to_int(self, hora_dia):
        """
        Convierte la hora del día a formato numérico que espera el ML service
        """
        if hasattr(hora_dia, 'value'):
            hora_str = hora_dia.value
        else:
            hora_str = str(hora_dia)
        
        hora_mapping = {
            'madrugada': 0,
            'mañana': 1, 
            'manana': 1,
            'tarde': 2,
            'noche': 3,
            'morning': 1,
            'afternoon': 2,
            'evening': 3,
            'night': 0
        }
        
        return hora_mapping.get(hora_str.lower(), 1) 