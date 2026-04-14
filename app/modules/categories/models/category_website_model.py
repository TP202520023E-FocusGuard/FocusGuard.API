from sqlalchemy import Column, Integer, String

from app.core.database import Base


class CategoryWebsiteModel(Base):
    __tablename__ = "categorias_web"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(25), nullable=False)
    codigo = Column(String(25), nullable=False)
    peso = Column(Integer, nullable=False)