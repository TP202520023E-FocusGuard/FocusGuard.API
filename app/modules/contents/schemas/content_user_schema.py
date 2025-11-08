from pydantic import BaseModel


class ContentUserBase(BaseModel):
    id_usuarios: int
    id_sitios_web_usuario: int
    id_contenidos: int
    id_categorias_contenido: int


class ContentUserCreate(ContentUserBase):
    pass

class ContentUserUpdate(BaseModel):
    id_categorias_contenido: int

class ContentUserResponse(ContentUserBase):
    id: int

    class Config:
        from_attributes = True