from sqlalchemy import String, DateTime, Integer, ForeignKey, Boolean, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class ClasificacionOrigen(enum.Enum):
    sistema = "sistema"
    equipo = "equipo"
    ml = "ml"

class FuenteClasificacion(enum.Enum):
    base = "base"
    personal = "personal" 
    ml = "ml"

class PatronUso(enum.Enum):
    rapido = "rapido"
    medio = "medio"
    prolongado = "prolongado"

class DiaSemana(enum.Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"

class ClassificationModel(Base):
    __tablename__ = "Clasificacion"
    
    id_clasificacion: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    nivel_prioridad: Mapped[int] = mapped_column(Integer, nullable=False)
    es_procrastinacion: Mapped[bool] = mapped_column(Boolean, default=False)
    color: Mapped[str] = mapped_column(String(7), default='#666666')

class SiteBaseModel(Base):
    __tablename__ = "Sitios_Base"
    
    id_sitio: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dominio: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=True)
    id_clasificacion: Mapped[int] = mapped_column(Integer, ForeignKey("Clasificacion.id_clasificacion"), nullable=False)
    es_curated: Mapped[bool] = mapped_column(Boolean, default=True)
    clasificacion_origen: Mapped[ClasificacionOrigen] = mapped_column(Enum(ClasificacionOrigen), default=ClasificacionOrigen.sistema)
    fecha_registro: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    
    clasificacion: Mapped["ClassificationModel"] = relationship("ClassificationModel")
    clasificaciones_usuario: Mapped[list["UserClassificationModel"]] = relationship("UserClassificationModel", back_populates="sitio")

class UserSiteModel(Base):
    __tablename__ = "Sitios_Usuario"
    
    id_sitio_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    dominio: Mapped[str] = mapped_column(String(255), nullable=False)
    id_clasificacion: Mapped[int] = mapped_column(Integer, ForeignKey("Clasificacion.id_clasificacion"), nullable=False)
    fecha_deteccion: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    
    clasificacion: Mapped["ClassificationModel"] = relationship("ClassificationModel")

class UserClassificationModel(Base):
    __tablename__ = "Clasificacion_Usuario"
    
    id_clasif: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    id_sitio: Mapped[int] = mapped_column(Integer, ForeignKey("Sitios_Base.id_sitio"), nullable=False)
    id_clasificacion: Mapped[int] = mapped_column(Integer, ForeignKey("Clasificacion.id_clasificacion"), nullable=False)
    fecha: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    
    sitio: Mapped["SiteBaseModel"] = relationship("SiteBaseModel", back_populates="clasificaciones_usuario")
    clasificacion: Mapped["ClassificationModel"] = relationship("ClassificationModel")

class NavigationHistoryModel(Base):
    __tablename__ = "Historial_Navegacion"
    
    id_historial: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    dominio: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_inicio: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    fecha_fin: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    duracion_segundos: Mapped[int] = mapped_column(Integer, default=0)
    dia_semana: Mapped[DiaSemana] = mapped_column(Enum(DiaSemana), nullable=False)
    hora_dia: Mapped[int] = mapped_column(Integer, nullable=False)
    es_fin_semana: Mapped[bool] = mapped_column(Boolean, default=False)
    id_clasificacion_aplicada: Mapped[int] = mapped_column(Integer, ForeignKey("Clasificacion.id_clasificacion"), nullable=False)
    fuente_clasificacion: Mapped[FuenteClasificacion] = mapped_column(Enum(FuenteClasificacion), default=FuenteClasificacion.base)
    patron_uso: Mapped[PatronUso] = mapped_column(Enum(PatronUso), default=PatronUso.medio)
    contexto_anterior: Mapped[str] = mapped_column(String(100), nullable=True)
    fue_bloqueado: Mapped[bool] = mapped_column(Boolean, default=False)
    usuario_ignoro_advertencia: Mapped[bool] = mapped_column(Boolean, default=False)
    
    clasificacion_aplicada: Mapped["ClassificationModel"] = relationship("ClassificationModel")