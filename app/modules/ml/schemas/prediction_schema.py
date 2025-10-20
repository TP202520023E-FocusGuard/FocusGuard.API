from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class MLPredictionResponse(BaseModel):
    id_prediccion: int
    user_id: str
    modelo_tipo: str
    focus_level: Optional[float]
    needs_intervention: bool
    confidence: Optional[float]
    predicted_duration: Optional[int]
    risk_factors: List[str]
    sequence_stats: Dict[str, Any]
    fecha_prediccion: datetime

    class Config:
        from_attributes = True