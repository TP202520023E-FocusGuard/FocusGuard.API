from sqlalchemy.ext.asyncio import AsyncSession
from .prediction_service import PredictionService

class MLService:
    def __init__(self, session: AsyncSession):
        self.prediction_service = PredictionService(session)
    
    async def generate_and_store_prediction(self, user_id: int):
        """
        🔹 Fachada para generar y almacenar predicciones ML
        """
        return await self.prediction_service.generate_and_store_prediction(user_id)