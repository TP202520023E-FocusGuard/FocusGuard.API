from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Request Schemas
class WeeklyGoalCreate(BaseModel):
    id_usuarios: int
    opcion_1: int  # 1: Más, 2: Menos
    tiempo: int    # Tiempo en minutos
    opcion_2: int  # 1: Categorización de sitio, 2: Categorización de contenido
    opcion_3: str  # ID de categoría como string
    fecha_limite: datetime

    model_config = ConfigDict(from_attributes=True)

class WeeklyGoalUpdate(BaseModel):
    opcion_1: Optional[int] = None
    tiempo: Optional[int] = None
    opcion_2: Optional[int] = None
    opcion_3: Optional[str] = None
    fecha_limite: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Response Schema
class WeeklyGoalResponse(BaseModel):
    id: int
    id_usuarios: int
    opcion_1: int
    tiempo: int
    opcion_2: int
    opcion_3: str
    fecha_limite: datetime

    model_config = ConfigDict(from_attributes=True)