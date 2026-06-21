from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WebsiteVisitedBase(BaseModel):
    id_usuarios: int
    id_sitios_web_usuario: int
    id_categorias_web: int
    fecha_hora_ingreso: datetime
    fecha_hora_salida: Optional[datetime] = None


class WebsiteVisitedCreate(WebsiteVisitedBase):
    pass

class WebsiteVisitedUpdate(BaseModel):
    fecha_hora_salida: datetime


class WebsiteVisitedResponse(WebsiteVisitedBase):
    id: int

    class Config:
        from_attributes = True

class WebsiteVisitedSummary(BaseModel):
    domain: str
    total_minutes: float
    total_visits: int
    first_visit: datetime
    last_visit: datetime
    category: str