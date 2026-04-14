from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WebsiteVisitedBase(BaseModel):
    id_usuarios: int
    id_sitios_web_usuario: int
    fecha_hora_ingreso: datetime
    fecha_hora_salida: Optional[datetime] = None
    id_categorias_web_snapshot: Optional[int] = None

class WebsiteVisitedCreate(WebsiteVisitedBase):
    pass

class WebsiteVisitedUpdate(BaseModel):
    fecha_hora_salida: datetime


class WebsiteVisitedResponse(WebsiteVisitedBase):
    id: int

    class Config:
        from_attributes = True