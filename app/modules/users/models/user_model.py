from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint, func

from app.core.database import Base


class UserModel(Base):
    __tablename__ = "usuarios"
    __table_args__ = (
        UniqueConstraint(
            "correo",
            name="UK_usuarios_correo",
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    correo = Column(String(100), nullable=False, index=True)
    contrasenia_hash = Column(String(255), nullable=False)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    telefono = Column(String(15), nullable=False)
    fecha_registro = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )