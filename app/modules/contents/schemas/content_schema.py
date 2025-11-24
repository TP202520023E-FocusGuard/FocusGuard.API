from pydantic import BaseModel, Field


class ContentBase(BaseModel):
    titulo: str = Field(..., max_length=255)
    descripcion: str | None = None
    twitter_cards: str | None = None


class ContentCreate(ContentBase):
    pass


class ContentResponse(ContentBase):
    id: int

    class Config:
        from_attributes = True