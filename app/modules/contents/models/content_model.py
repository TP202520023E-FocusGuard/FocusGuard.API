from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class ContentModel(Base):
    __tablename__ = "contenidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=True)
    descripcion = Column(Text, nullable=True)
    twitter_cards = Column(Text, nullable=True)