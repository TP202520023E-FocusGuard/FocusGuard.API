from sqlalchemy import Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base

class DailyProgressModel(Base):
    __tablename__ = "objetivos_diarios_alcanzados"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_objetivos_semanales: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("objetivos_semanales.id"), 
        nullable=False
    )
    tiempo_alcanzado: Mapped[int] = mapped_column(Integer, nullable=False)  # Minutos alcanzados
    es_alcanzado: Mapped[bool] = mapped_column(Boolean, nullable=False)     # True/False
    fecha: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)