from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WebsiteVisitedBase(BaseModel):
    id_usuarios: int
    id_sitios_web_usuario: int
    fecha_hora_ingreso: datetime
    fecha_hora_salida: Optional[datetime] = None


class WebsiteVisitedCreate(WebsiteVisitedBase):
    pass


class WebsiteVisitedResponse(WebsiteVisitedBase):
    id_sitios_web_usuario: int
    fecha_hora_ingreso: datetime
    fecha_hora_salida: Optional[datetime] = None

    class Config:
        from_attributes = True