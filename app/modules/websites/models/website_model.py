from sqlalchemy import Column, Integer, String
from app.core.database import Base

class WebsiteModel(Base):
    __tablename__ = 'sitios_web'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dominio = Column(String(50), unique=True, nullable=False)


