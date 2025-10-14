from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ConfigurationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_config: int
    id_usuario: int
    tiempo_ocio_diario: int
    tiempo_max_productivo: int
    idioma: str
    bloqueo_automatico: bool
    fecha_actualizacion: datetime

class ConfigurationUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    tiempo_ocio_diario: Optional[int] = None
    tiempo_max_productivo: Optional[int] = None
    idioma: Optional[str] = None
    bloqueo_automatico: Optional[bool] = None

class ConfigurationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_config: int
    id_usuario: int
    tiempo_ocio_diario: int
    tiempo_max_productivo: int
    idioma: str
    bloqueo_automatico: bool
    fecha_actualizacion: datetime