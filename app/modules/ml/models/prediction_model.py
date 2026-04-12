from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey
from app.core.database import Base


class PrediccionSecuencial(Base):
    __tablename__ = "predicciones_secuencial"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    id_usuarios = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    ts_prediccion = Column(DateTime, nullable=False)

    horizonte_segundos = Column(Integer, nullable=False)

    prob_procrastinacion = Column(Float, nullable=False)

    umbral_decision = Column(Float, nullable=True)

    version_modelo = Column(String(50), nullable=False)

    features_hash = Column(String(64), nullable=False)

    is_procrastinating = Column(Boolean, nullable=True)