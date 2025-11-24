from sqlalchemy import Column, DateTime, ForeignKey, Integer

from app.core.database import Base


class ContentVisitedModel(Base):
    __tablename__ = "contenidos_visitados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuarios = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_contenidos_usuario = Column(
        Integer,
        ForeignKey("contenidos_usuario.id"),
        nullable=False,
    )
    fecha_hora_ingreso = Column(DateTime, nullable=False)
    fecha_hora_salida = Column(DateTime, nullable=True)