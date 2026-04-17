from sqlalchemy import Boolean, Column, Integer, String

from app.core.database import Base


class CategoryContentModel(Base):
    __tablename__ = "categorias_contenido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(25), nullable=False)
    codigo = Column(String(25), nullable=False)
    es_ocio = Column(Boolean, nullable=False)
    peso = Column(Integer, nullable=False)