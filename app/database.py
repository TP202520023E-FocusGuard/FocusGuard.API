from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. CADENA DE CONEXIÓN (DATABASE URL)
# Formato: mysql+mysqldb://USUARIO:CONTRASEÑA@HOST/NOMBRE_BD
DATABASE_URL = "mysql+mysqldb://root:root@localhost/focusguard"

# Puedes reemplazar 'localhost' con la IP de tu servidor MySQL.

# 2. CREAR EL ENGINE (MOTOR)
# El Engine es el punto de partida de SQLAlchemy, maneja la conexión.
# echo=True imprime las consultas SQL generadas en la consola (útil para debug).
engine = create_engine(
    DATABASE_URL,
    echo=False
)

# 3. CREAR LA FÁBRICA DE SESIONES
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Función de utilidad para obtener una sesión (usada por los servicios/controladores)
def get_db():
    """Genera una nueva sesión de base de datos para una petición."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()