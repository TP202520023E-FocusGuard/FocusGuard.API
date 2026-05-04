from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class InterventionCreate(BaseModel):
    id_usuarios: int
    id_metas: Optional[int] = None
    id_frases_motivadoras: Optional[int] = None
    id_experimentos_intervencion: Optional[int] = None
    tipo: int
    fecha_despliegue: datetime
    fecha_desbloqueo: Optional[datetime] = None
    rigurosidad: Optional[int] = None
    version_politica: Optional[str] = Field(default=None, max_length=50)
    variante: Optional[str] = Field(default=None, max_length=20)


class InterventionUpdateUnlockDate(BaseModel):
    fecha_desbloqueo: datetime


class InterventionResponse(InterventionCreate):
    id: int

    class Config:
        from_attributes = True


class IntAvisoCreate(BaseModel):
    id_intervenciones: int
    tiempo: int


class IntAvisoResponse(IntAvisoCreate):
    class Config:
        from_attributes = True


class IntBloqueoCreate(BaseModel):
    id_intervenciones: int
    tiempo: int


class IntBloqueoResponse(IntBloqueoCreate):
    class Config:
        from_attributes = True


class IntEscrituraCreate(BaseModel):
    id_intervenciones: int
    texto: str = Field(..., max_length=350)
    cant_carac: Optional[int] = None


class IntEscrituraResponse(IntEscrituraCreate):
    class Config:
        from_attributes = True