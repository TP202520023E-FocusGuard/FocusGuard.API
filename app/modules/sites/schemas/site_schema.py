from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class ClassificationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_clasificacion: int
    nombre: str
    descripcion: Optional[str] = None
    nivel_prioridad: int
    es_procrastinacion: bool
    color: str

class SiteBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_sitio: int
    dominio: str
    nombre: Optional[str] = None
    id_clasificacion: int
    es_curated: bool
    clasificacion_origen: str
    fecha_registro: datetime
    clasificacion: ClassificationBase

class UserSiteBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_sitio_usuario: int
    id_usuario: int
    dominio: str
    id_clasificacion: int
    fecha_deteccion: datetime
    clasificacion: ClassificationBase

class NavigationHistoryCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    dominio: str
    contexto_anterior: Optional[str] = None

class NavigationHistoryUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    duracion_segundos: int
    fue_bloqueado: Optional[bool] = False
    usuario_ignoro_advertencia: Optional[bool] = False

class CombinedSiteWithClassification(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_sitio: Optional[int] = None  # Solo para sitios base
    dominio: str
    nombre: str
    tipo_sitio: str  # 'base' o 'personal'
    clasificacion_global: ClassificationBase
    clasificacion_personal: Optional[ClassificationBase] = None
    usando_clasificacion: str  # 'global' o 'personal' 

class UnifiedClassificationUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    # Para sitios base
    id_sitio: Optional[int] = None
    # Para sitios personales  
    dominio: Optional[str] = None
    # Común
    id_clasificacion: int

class ClassificationResponse(BaseModel):
    """Respuesta simple para clasificación"""
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    message: str
    tipo_sitio: str  # 'base' o 'personal'

class UserClassificationCreate(BaseModel):
    id_sitio: int
    id_clasificacion: int

