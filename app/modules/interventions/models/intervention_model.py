from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.core.database import Base


class InterventionModel(Base):
    __tablename__ = 'intervenciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuarios = Column(Integer, nullable=False)
    id_metas = Column(Integer, nullable=True)
    id_frases_motivadoras = Column(Integer, nullable=True)
    id_experimentos_intervencion = Column(Integer, nullable=True)
    tipo = Column(Integer, nullable=False)
    fecha_despliegue = Column(TIMESTAMP, nullable=False)
    fecha_desbloqueo = Column(TIMESTAMP, nullable=True)
    rigurosidad = Column(Integer, nullable=True)
    version_politica = Column(String(50), nullable=True)
    variante = Column(String(20), nullable=True)


class IntAvisoModel(Base):
    __tablename__ = 'int_avisos'

    id_intervenciones = Column(Integer, primary_key=True, nullable=False)
    tiempo = Column(Integer, nullable=False)


class IntBloqueoModel(Base):
    __tablename__ = 'int_bloqueos'

    id_intervenciones = Column(Integer, primary_key=True, nullable=False)
    tiempo = Column(Integer, nullable=False)


class IntEscrituraModel(Base):
    __tablename__ = 'int_escrituras'

    id_intervenciones = Column(Integer, primary_key=True, nullable=False)
    texto = Column(String(350), nullable=False)
    cant_carac = Column(Integer, nullable=True)