from pydantic import BaseModel
from typing import List
from datetime import datetime

class MLInputItem(BaseModel):
    categoria: str                 
    duracion_segundos: int        


class MLInputPayload(BaseModel):
    user_id: int                  
    registros: List[MLInputItem]  

    class Config:
        from_attributes = True   