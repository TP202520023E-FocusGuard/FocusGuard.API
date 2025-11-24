from pydantic import BaseModel, Field


class WebsiteUserBase(BaseModel):
    id_usuarios: int
    id_sitios_web: int
    id_categorias_web: int
    origen: str = Field(default="custom", max_length=50)


class WebsiteUserCreate(WebsiteUserBase):
    pass

class WebsiteUserUpdate(BaseModel):
    id_categorias_web: int

class WebsiteUserResponse(WebsiteUserBase):
    id: int
    id_sitios_web: int
    id_categorias_web: int

    class Config:
        from_attributes = True

class WebsiteUserListResponse(BaseModel):
    id: int
    dominio: str
    categoria: str