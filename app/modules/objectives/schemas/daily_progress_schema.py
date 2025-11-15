from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Request Schemas
class DailyProgressCreate(BaseModel):
    id_objetivos_semanales: int
    tiempo_alcanzado: int      # Minutos alcanzados
    es_alcanzado: bool         # True/False

    model_config = ConfigDict(from_attributes=True)

class DailyProgressUpdate(BaseModel):
    tiempo_alcanzado: Optional[int] = None
    es_alcanzado: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

# Response Schema
class DailyProgressResponse(BaseModel):
    id: int
    id_objetivos_semanales: int
    tiempo_alcanzado: int
    es_alcanzado: bool
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)