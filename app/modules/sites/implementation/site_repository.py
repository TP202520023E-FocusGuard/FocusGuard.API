from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, text
from sqlalchemy.orm import selectinload
from typing import List, Optional, Tuple
from datetime import datetime
from app.modules.sites.models.site_model import (
    SiteBaseModel, UserSiteModel, UserClassificationModel, 
    ClassificationModel, NavigationHistoryModel
)
from app.modules.sites.schemas.site_schema import (
    UserClassificationCreate, NavigationHistoryCreate, NavigationHistoryUpdate
)
from app.core.exceptions import DatabaseException, NotFoundException

class SiteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_combined_sites_with_classification(self, user_id: int) -> List[Tuple]:
        """
        Obtiene sitios CURADOS + PERSONALES con sus clasificaciones
        en un solo query
        """
        try:
            query = text("""
                -- Sitios CURADOS (Sitios_Base)
                SELECT 
                    sb.id_sitio, sb.dominio, sb.nombre,
                    -- Clasificación global
                    cg.id_clasificacion as global_id, 
                    cg.nombre as global_nombre, 
                    cg.descripcion as global_descripcion, 
                    cg.nivel_prioridad as global_prioridad,
                    cg.es_procrastinacion as global_es_procrastinacion, 
                    cg.color as global_color,
                    -- Clasificación personal (si existe)
                    cp.id_clasificacion as personal_id, 
                    cp.nombre as personal_nombre,
                    cp.descripcion as personal_descripcion, 
                    cp.nivel_prioridad as personal_prioridad,
                    cp.es_procrastinacion as personal_es_procrastinacion, 
                    cp.color as personal_color,
                    'base' as tipo_sitio
                FROM Sitios_Base sb
                INNER JOIN Clasificacion cg ON sb.id_clasificacion = cg.id_clasificacion
                LEFT JOIN Clasificacion_Usuario uc ON 
                    sb.id_sitio = uc.id_sitio AND uc.id_usuario = :user_id
                LEFT JOIN Clasificacion cp ON uc.id_clasificacion = cp.id_clasificacion
                
                UNION ALL
                
                -- Sitios PERSONALES (Sitios_Usuario)
                SELECT 
                    NULL as id_sitio,
                    su.dominio, 
                    su.dominio as nombre,
                    5 as global_id, 
                    'sin_clasificar' as global_nombre,
                    NULL as global_descripcion,
                    5 as global_prioridad,
                    FALSE as global_es_procrastinacion,
                    '#9CA3AF' as global_color,
                    cp.id_clasificacion as personal_id, 
                    cp.nombre as personal_nombre,
                    cp.descripcion as personal_descripcion, 
                    cp.nivel_prioridad as personal_prioridad,
                    cp.es_procrastinacion as personal_es_procrastinacion, 
                    cp.color as personal_color,
                    'personal' as tipo_sitio
                FROM Sitios_Usuario su
                INNER JOIN Clasificacion cp ON su.id_clasificacion = cp.id_clasificacion
                WHERE su.id_usuario = :user_id
                
                ORDER BY dominio
            """)
            
            result = await self.session.execute(query, {"user_id": user_id})
            return result.all()
            
        except Exception as e:
            raise DatabaseException(f"Error getting combined sites: {str(e)}")

    async def get_all_classifications(self) -> List[ClassificationModel]:
        try:
            result = await self.session.execute(
                select(ClassificationModel).order_by(ClassificationModel.nivel_prioridad)
            )
            return result.scalars().all()
        except Exception as e:
            raise DatabaseException(f"Error getting classifications: {str(e)}")

    async def get_site_base_by_domain(self, dominio: str) -> Optional[SiteBaseModel]:
        try:
            result = await self.session.execute(
                select(SiteBaseModel)
                .options(selectinload(SiteBaseModel.clasificacion))
                .where(SiteBaseModel.dominio == dominio)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            raise DatabaseException(f"Error getting site by domain: {str(e)}")

    async def get_site_base_by_id(self, id_sitio: int) -> Optional[SiteBaseModel]:
        try:
            result = await self.session.execute(
                select(SiteBaseModel)
                .options(selectinload(SiteBaseModel.clasificacion))
                .where(SiteBaseModel.id_sitio == id_sitio)
            )
            site = result.scalar_one_or_none()
            if not site:
                raise NotFoundException(f"Site with id {id_sitio} not found")
            return site
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error getting site by id: {str(e)}")

    async def get_user_classification(self, user_id: int, id_sitio: int) -> Optional[UserClassificationModel]:
        try:
            result = await self.session.execute(
                select(UserClassificationModel)
                .options(
                    selectinload(UserClassificationModel.sitio).selectinload(SiteBaseModel.clasificacion),
                    selectinload(UserClassificationModel.clasificacion)
                )
                .where(and_(
                    UserClassificationModel.id_usuario == user_id,
                    UserClassificationModel.id_sitio == id_sitio
                ))
            )
            return result.scalar_one_or_none()
        except Exception as e:
            raise DatabaseException(f"Error getting user classification: {str(e)}")

    async def save_user_classification(self, user_classification: UserClassificationCreate, user_id: int) -> UserClassificationModel:
        try:
            # Verificar si ya existe
            existing = await self.get_user_classification(user_id, user_classification.id_sitio)
            
            if existing:
                # Actualizar existente
                existing.id_clasificacion = user_classification.id_clasificacion
                existing.fecha = datetime.now()
                await self.session.commit()
                await self.session.refresh(existing)
                return existing
            else:
                # Crear nuevo
                new_classification = UserClassificationModel(
                    id_usuario=user_id,
                    id_sitio=user_classification.id_sitio,
                    id_clasificacion=user_classification.id_clasificacion
                )
                self.session.add(new_classification)
                await self.session.commit()
                
                # Recargar con relaciones
                await self.session.refresh(new_classification)
                result = await self.session.execute(
                    select(UserClassificationModel)
                    .options(
                        selectinload(UserClassificationModel.sitio).selectinload(SiteBaseModel.clasificacion),
                        selectinload(UserClassificationModel.clasificacion)
                    )
                    .where(UserClassificationModel.id_clasif == new_classification.id_clasif)
                )
                return result.scalar_one()
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(f"Error saving user classification: {str(e)}")

    async def get_or_create_user_site(self, user_id: int, dominio: str) -> UserSiteModel:
        """Obtiene o crea un sitio personal para el usuario"""
        try:
            # Verificar si ya existe
            result = await self.session.execute(
                select(UserSiteModel)
                .where(and_(
                    UserSiteModel.id_usuario == user_id,
                    UserSiteModel.dominio == dominio
                ))
            )
            user_site = result.scalar_one_or_none()
            
            if user_site:
                return user_site
            else:
                # Crear nuevo sitio personal
                return await self._create_user_site(user_id, dominio, 5)  # 5 = 'sin_clasificar'
                
        except Exception as e:
            raise DatabaseException(f"Error getting/creating user site: {str(e)}")

    async def update_user_site_classification(self, user_id: int, dominio: str, id_clasificacion: int) -> UserSiteModel:
        """Actualiza clasificación de sitio personal"""
        try:
            result = await self.session.execute(
                select(UserSiteModel)
                .where(and_(
                    UserSiteModel.id_usuario == user_id,
                    UserSiteModel.dominio == dominio
                ))
            )
            user_site = result.scalar_one_or_none()
            
            if not user_site:
                raise NotFoundException(f"User site not found for user {user_id} and domain {dominio}")
            
            user_site.id_clasificacion = id_clasificacion
            await self.session.commit()
            await self.session.refresh(user_site)
            return user_site
            
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(f"Error updating user site classification: {str(e)}")

    async def create_navigation_history(self, history_data: NavigationHistoryCreate, user_id: int, id_clasificacion: int) -> NavigationHistoryModel:
        try:
            now = datetime.now()
            
            history = NavigationHistoryModel(
                id_usuario=user_id,
                dominio=history_data.dominio,
                id_clasificacion_aplicada=id_clasificacion,
                contexto_anterior=history_data.contexto_anterior,
                dia_semana=now.strftime('%A').lower(),
                hora_dia=now.hour,
                es_fin_semana=now.weekday() >= 5
            )
            self.session.add(history)
            await self.session.commit()
            await self.session.refresh(history)
            return history
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(f"Error creating navigation history: {str(e)}")

    async def update_navigation_history(self, history_id: int, update_data: NavigationHistoryUpdate) -> Optional[NavigationHistoryModel]:
        try:
            result = await self.session.execute(
                select(NavigationHistoryModel)
                .options(selectinload(NavigationHistoryModel.clasificacion_aplicada))
                .where(NavigationHistoryModel.id_historial == history_id)
            )
            history = result.scalar_one_or_none()
            
            if history:
                history.fecha_fin = datetime.now()
                history.duracion_segundos = update_data.duracion_segundos
                history.fue_bloqueado = update_data.fue_bloqueado
                history.usuario_ignoro_advertencia = update_data.usuario_ignoro_advertencia
                
                await self.session.commit()
                await self.session.refresh(history)
                return history
            return None
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(f"Error updating navigation history: {str(e)}")

    # Método privado para crear sitios de usuario (solo usado internamente)
    async def _create_user_site(self, user_id: int, dominio: str, id_clasificacion: int) -> UserSiteModel:
        """Método interno para crear sitios de usuario"""
        try:
            user_site = UserSiteModel(
                id_usuario=user_id,
                dominio=dominio,
                id_clasificacion=id_clasificacion
            )
            self.session.add(user_site)
            await self.session.commit()
            await self.session.refresh(user_site)
            return user_site
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(f"Error creating user site: {str(e)}")