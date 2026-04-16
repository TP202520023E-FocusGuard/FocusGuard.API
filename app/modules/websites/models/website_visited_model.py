from sqlalchemy import Column, DateTime, ForeignKey, Integer
from app.core.database import Base


class WebsiteVisitedModel(Base):
    __tablename__ = "sitios_web_visitados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuarios = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_sitios_web_usuario = Column(
        Integer,
        ForeignKey("sitios_web_usuario.id"),
        nullable=False,
    )
    fecha_hora_ingreso = Column(DateTime, nullable=False)
    fecha_hora_salida = Column(DateTime, nullable=True)
    id_categorias_web = Column(Integer, ForeignKey("categorias_web.id"), nullable=True)