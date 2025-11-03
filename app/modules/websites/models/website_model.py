from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Base para todos los modelos ORM
Base = declarative_base()

class WebsiteModel(Base):
    __tablename__ = 'sitios_web'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dominio = Column(String(100), unique=True)












