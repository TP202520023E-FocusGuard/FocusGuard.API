from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ContentVisitedBase(BaseModel):
    id_usuarios: int
    id_contenidos_usuario: int
    fecha_hora_ingreso: datetime
    fecha_hora_salida: Optional[datetime] = None


class ContentVisitedCreate(ContentVisitedBase):
    pass


class ContentVisitedResponse(ContentVisitedBase):
    id: int

    class Config:
        from_attributes = True