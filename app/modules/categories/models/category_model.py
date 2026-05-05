from sqlalchemy import String, Text, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base

class CategoryBaseModel(Base):
    __tablename__ = "Categorias_Base"
    
    id_categoria: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    
    categorias_usuario: Mapped[list["CategoryUserModel"]] = relationship(
        "CategoryUserModel", back_populates="categoria_base"
    )

class CategoryUserModel(Base):
    __tablename__ = "Categorias_Usuario"
    
    id_cat_user: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    id_categoria: Mapped[int] = mapped_column(Integer, ForeignKey("Categorias_Base.id_categoria"), nullable=False)  # ✅ AGREGAR FOREIGN KEY
    es_procrastinacion: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    categoria_base: Mapped["CategoryBaseModel"] = relationship(
        "CategoryBaseModel", back_populates="categorias_usuario"
    )

class ChangeCategoryModel(Base):
    __tablename__ = "cambios_categoria"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuarios: Mapped[int] = mapped_column(Integer, nullable=False)
    id_sitios_web_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("sitios_web_usuario.id"), nullable=False)
    id_categorias_web_anterior: Mapped[int] = mapped_column(Integer, ForeignKey("categorias_web.id"), nullable=False)
    id_categorias_web_nuevo: Mapped[int] = mapped_column(Integer, ForeignKey("categorias_web.id"), nullable=False)
    fecha_hora: Mapped[DateTime] = mapped_column(DateTime, default=func.now())