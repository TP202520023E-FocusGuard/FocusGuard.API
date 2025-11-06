from pydantic import BaseModel, Field


class CategoryWebsiteCreate(BaseModel):
    nombre: str = Field(..., max_length=25)
    peso: int = Field(..., ge=1, le=5)


class CategoryWebsiteResponse(CategoryWebsiteCreate):
    id: int
    pass

    class Config:
        from_attributes = True