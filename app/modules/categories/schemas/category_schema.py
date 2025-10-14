from pydantic import BaseModel, ConfigDict
from typing import Optional, List

# Request Schemas
class CategoriaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_categoria: int
    nombre: str
    descripcion: Optional[str] = None

class CategoriaUsuarioCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_categoria: int
    es_procrastinacion: bool

class CategoriaUsuarioUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    categorias: List[CategoriaUsuarioCreate]

# Response Schemas  
class CategoriaConSeleccion(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_categoria: int
    nombre: str
    descripcion: Optional[str] = None
    es_procrastinacion: Optional[bool] = None