from pydantic import BaseModel, Field


class CategoryContentBase(BaseModel):
    nombre: str = Field(..., max_length=25)
    es_ocio: bool
    peso: int


class CategoryContentCreate(CategoryContentBase):
    pass


class CategoryContentResponse(CategoryContentBase):
    id: int
    pass

    class Config:
        from_attributes = True