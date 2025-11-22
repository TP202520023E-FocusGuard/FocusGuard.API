from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, text
from app.core.database import Base


class WebsiteUserModel(Base):
    __tablename__ = "sitios_web_usuario"
    __table_args__ = (
        UniqueConstraint(
            "id_usuarios",
            "id_sitios_web",
            name="UK_sitios_web_usuario_composite",
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuarios = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_sitios_web = Column(Integer, ForeignKey("sitios_web.id"), nullable=False)
    id_categorias_web = Column(Integer, ForeignKey("categorias_web.id"), nullable=False)
    origen = Column(
        String(50),
        nullable=False,
        default="custom",
        server_default=text("'custom'")
    )