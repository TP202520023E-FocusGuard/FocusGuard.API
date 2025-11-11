from pydantic import BaseModel, ConfigDict
from typing import Optional

# Request Schemas
class GoalCreate(BaseModel):
    id_usuarios: int
    texto: str

    model_config = ConfigDict(from_attributes=True)

class GoalUpdate(BaseModel):
    texto: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Response Schema
class GoalResponse(BaseModel):
    id: int
    id_usuarios: int
    texto: str

    model_config = ConfigDict(from_attributes=True)