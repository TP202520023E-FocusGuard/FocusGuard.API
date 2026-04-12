from pydantic import BaseModel
from typing import List
from datetime import datetime

class RegistroSchema(BaseModel):
    categoria: str
    duracion_segundos: float


class PrediccionRequest(BaseModel):
    id_usuario: int


class PrediccionResponse(BaseModel):
    id_prediccion: int
    id_usuario: int

    prob_procrastinacion: float
    is_procrastinating: bool

    umbral_decision: float
    version_modelo: str
    horizonte_segundos: int

    ts_prediccion: datetime

    class Config:
        from_attributes = True