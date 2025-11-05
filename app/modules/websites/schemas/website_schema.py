from pydantic import BaseModel, Field
from typing import Optional

class WebsiteCreate(BaseModel):
    dominio: str = Field(max_length=100)

class WebsiteResponse(WebsiteCreate):
    id: int

    class Config:
        from_attributes = True