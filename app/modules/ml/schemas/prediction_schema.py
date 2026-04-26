from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RegistroSchema(BaseModel):
    categoria: str
    duracion_segundos: float


class PrediccionRequest(BaseModel):
    id_usuarios: int


class PrediccionResponse(BaseModel):
    id: int
    id_usuarios: int

    prob_procrastinacion: float
    is_procrastinating: bool

    umbral_decision: float
    version_modelo: str
    horizonte_segundos: int

    ts_prediccion: datetime

    class Config:
        from_attributes = True


class DecisionMLResponse(BaseModel):
    # --- salida TF ---
    prob_procrastinacion: float
    is_procrastinating: bool

    # --- salida DQN ---
    action: str
    raw_action: Optional[int] = None
    q_values: Optional[List[float]] = None
    source: str

    # --- metadata ---
    umbral_decision: float
    version_modelo: str
    horizonte_segundos: int