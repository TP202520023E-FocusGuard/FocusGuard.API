from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class RestTimeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    id_usuarios: int
    tiempo_total: int
    tiempo_usado: int
    fecha_actualizacion: date


class RestTimeUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    tiempo_total: Optional[int] = None
    tiempo_usado: Optional[int] = None


class RestTimeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    id_usuarios: int
    tiempo_total: int
    tiempo_usado: int
    fecha_actualizacion: date