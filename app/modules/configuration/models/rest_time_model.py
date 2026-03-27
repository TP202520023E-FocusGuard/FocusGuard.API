from sqlalchemy import DateTime, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base

class RestTimeModel(Base):
    __tablename__ = "tiempos_descanso"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_usuarios: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"))
    tiempo_total: Mapped[int] = mapped_column(Integer, default=120)