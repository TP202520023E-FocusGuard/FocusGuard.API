from sqlalchemy import Boolean, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base

class WeeklyGoalModel(Base):
    __tablename__ = "objetivos_semanales"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuarios: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    opcion_1: Mapped[int] = mapped_column(Integer, nullable=False)  # 1: Más, 2: Menos
    tiempo: Mapped[int] = mapped_column(Integer, nullable=False)    # Tiempo en minutos
    opcion_2: Mapped[int] = mapped_column(Integer, nullable=False)  # 1: Categorización de sitio, 2: Categorización de contenido
    opcion_3: Mapped[str] = mapped_column(String(100), nullable=False)  # 'productivo', 'distractor', 'ocio', etc.
    fecha_inicio: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    fecha_limite: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    completado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)