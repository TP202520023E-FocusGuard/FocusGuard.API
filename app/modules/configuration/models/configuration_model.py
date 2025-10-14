from sqlalchemy import DateTime, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base

class ConfigurationModel(Base):
    __tablename__ = "Configuracion"
    
    id_config: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    tiempo_ocio_diario: Mapped[int] = mapped_column(Integer, default=120)  # minutos
    tiempo_max_productivo: Mapped[int] = mapped_column(Integer, default=60)  # minutos
    idioma: Mapped[str] = mapped_column(String(10), default='es')
    bloqueo_automatico: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())