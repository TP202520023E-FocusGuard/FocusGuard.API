from sqlalchemy import String, Integer, ForeignKey, DateTime
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
    opcion_3: Mapped[str] = mapped_column(String(100), nullable=False)  # ID de categoría como string
    fecha_limite: Mapped[DateTime] = mapped_column(DateTime, nullable=False)