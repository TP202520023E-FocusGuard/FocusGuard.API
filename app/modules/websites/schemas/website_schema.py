from pydantic import BaseModel, Field

class WebsiteCreate(BaseModel):
    dominio: str = Field(..., max_length=50)

class WebsiteResponse(WebsiteCreate):
    id: int

    class Config:
        from_attributes = True