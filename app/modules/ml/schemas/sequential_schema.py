from pydantic import BaseModel
from typing import List
from datetime import datetime

class MLInputItem(BaseModel):
    categoria: str                 # nombre de la categoría vigente
    duracion_segundos: int         # tiempo de estancia en esa categoría (segundos)


class MLInputPayload(BaseModel):
    user_id: int                   # id del usuario
    registros: List[MLInputItem]   # lista de los últimos 10 registros

    class Config:
        from_attributes = True     # permite construir desde objetos ORM