from sqlalchemy import Column, Integer, String, UniqueConstraint, Text

from app.core.database import Base


class ContentModel(Base):
    __tablename__ = "contenidos"
    __table_args__ = (
        UniqueConstraint(
            "titulo",
            name="UK_contenidos_titulo",
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    twitter_cards = Column(Text, nullable=True)