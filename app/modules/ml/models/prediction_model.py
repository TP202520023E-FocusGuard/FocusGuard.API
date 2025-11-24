from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, ForeignKey, Text, Enum as SQLEnum
from datetime import datetime
from app.core.database import Base

class MLPredictionLog(Base):
    __tablename__ = "ml_prediction_log"
    
    id_prediccion = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False)
    modelo_tipo = Column(SQLEnum('contextual', 'predictivo', 'secuencial'), nullable=False)
    fecha_prediccion = Column(DateTime, default=datetime.now)

    focus_level = Column(Float, nullable=True)
    needs_intervention = Column(Boolean, default=False)
    confidence = Column(Float, nullable=True)
    predicted_duration = Column(Integer, nullable=True)
    risk_factors = Column(JSON, nullable=True)
    sequence_stats = Column(JSON, nullable=True)
    
    source_ip = Column(String(45), nullable=True)
    ejecutado_por = Column(String(100), nullable=True)
    observaciones = Column(Text, nullable=True)

class PrediccionHistorial(Base):
    __tablename__ = "prediccion_historial"
    
    id_relacion = Column(Integer, primary_key=True, autoincrement=True)
    id_prediccion = Column(Integer, ForeignKey("ml_prediction_log.id_prediccion", ondelete="CASCADE"))
    id_historial = Column(Integer, ForeignKey("historial_navegacion.id_historial", ondelete="CASCADE"))