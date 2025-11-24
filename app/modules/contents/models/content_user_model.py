from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from app.core.database import Base


class ContentUserModel(Base):
    __tablename__ = "contenidos_usuario"
    __table_args__ = (
        UniqueConstraint(
            "id_usuarios",
            "id_sitios_web_usuario",
            "id_contenidos",
            name="UK_contenidos_usuario_composite",
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuarios = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False,
    )
    id_sitios_web_usuario = Column(
        Integer,
        ForeignKey("sitios_web_usuario.id"),
        nullable=False,
    )
    id_contenidos = Column(
        Integer,
        ForeignKey("contenidos.id"),
        nullable=False,
    )
    id_categorias_contenido = Column(
        Integer,
        ForeignKey("categorias_contenido.id"),
        nullable=False,
    )