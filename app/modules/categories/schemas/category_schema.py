from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# Request Schemas
class ChangeCategory(BaseModel):
    id: int
    id_usuarios: int
    id_sitios_web_usuario: int
    id_categorias_web_anterior: int
    id_categorias_web_nuevo: int
    fecha_hora: datetime

    model_config = ConfigDict(from_attributes=True)

class ChangeCategoryCreate(BaseModel):
    id_usuarios: int
    id_sitios_web_usuario: int
    id_categorias_web_nuevo: int