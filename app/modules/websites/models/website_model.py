from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, func
from app.core.database import Base

class WebsiteModel(Base):
    __tablename__ = 'sitios_web'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dominio = Column(String(50), unique=True, nullable=False)


class WebsiteglobalModel(Base):
    __tablename__ = 'sitios_web_global'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_sitios_web = Column(Integer, nullable=False)
    id_categorias_web = Column(Integer, nullable=False)
    confianza = Column(DECIMAL(4,3), nullable=False)
    fecha_actualizacion = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
