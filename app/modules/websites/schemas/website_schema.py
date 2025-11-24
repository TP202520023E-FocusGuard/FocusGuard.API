from pydantic import BaseModel, Field
from datetime import datetime

class WebsiteCreate(BaseModel):
    dominio: str = Field(..., max_length=50)

class WebsiteResponse(WebsiteCreate):
    id: int

    class Config:
        from_attributes = True

class WebsiteGlobalResponse(BaseModel):
    id: int
    id_sitios_web: int
    id_categorias_web: int
    confianza: float
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True