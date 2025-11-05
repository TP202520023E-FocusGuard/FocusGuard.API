from typing import Optional

#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.website_model import WebsiteModel
from ..schemas.website_schema import WebsiteCreate

class WebsiteRepository:

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    def create(self, data: WebsiteCreate) -> Optional[WebsiteModel]:
        """Crea una categoría usando SQLAlchemy ORM."""

        # 1. CREACIÓN DIRECTA DEL OBJETO MAPPEDO
        nuevo_website = WebsiteModel(
            dominio=data.dominio,
        )

        try:
            # 2. AGREGA A LA SESIÓN (Pendiente de guardado)
            self.db.add(nuevo_website)

            # 3. EJECUCIÓN Y GESTIÓN DE LA TRANSACCIÓN
            self.db.commit()

            # 4. ACTUALIZA EL OBJETO CON EL ID (automático por SQLAlchemy)
            self.db.refresh(nuevo_website)

            # 5. DEVUELVE EL OBJETO PYTHON COMPLETO
            return nuevo_website

        except Exception as e:
            # Manejo de errores de base de datos
            self.db.rollback()
            print(f"Error al crear: {e}")
            return None