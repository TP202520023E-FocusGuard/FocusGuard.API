from pydantic import BaseModel, Field


class CategoryWebsiteCreate(BaseModel):
    nombre: str = Field(..., max_length=25)
    peso: int


class CategoryWebsiteResponse(CategoryWebsiteCreate):
    id: int
    pass

    class Config:
        from_attributes = True