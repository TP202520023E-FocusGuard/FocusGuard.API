from pydantic import BaseModel, ConfigDict
from typing import Optional

class RestTimeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    id_usuarios: int
    tiempo_total: int


class RestTimeUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    tiempo_total: Optional[int] = None


class RestTimeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    id_usuarios: int
    tiempo_total: int