from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.sites.implementation.site_repository import SiteRepository
from app.modules.sites.schemas.site_schema import (
    ClassificationBase, CombinedSiteWithClassification,
    NavigationHistoryCreate, NavigationHistoryUpdate, 
    UnifiedClassificationUpdate, ClassificationResponse,
    SiteClassificationUpdate
)
from app.core.exceptions import BusinessException, ValidationException, NotFoundException

class SiteService:
    def __init__(self, session: AsyncSession):
        self.repository = SiteRepository(session)

    # LISTA PRINCIPAL - Sitios curados + personales
    async def get_combined_sites_with_classification(self, user_id: int) -> List[CombinedSiteWithClassification]:
        """Obtiene sitios CURADOS + PERSONALES con clasificaciones"""
        try:
            rows = await self.repository.get_combined_sites_with_classification(user_id)
            result = []
            
            for row in rows:
                # Clasificación global
                global_classification = ClassificationBase(
                    id_clasificacion=row.global_id,
                    nombre=row.global_nombre,
                    descripcion=row.global_descripcion,
                    nivel_prioridad=row.global_prioridad,
                    es_procrastinacion=bool(row.global_es_procrastinacion),
                    color=row.global_color
                )
                
                # Clasificación personal
                personal_classification = None
                if row.personal_id:
                    personal_classification = ClassificationBase(
                        id_clasificacion=row.personal_id,
                        nombre=row.personal_nombre,
                        descripcion=row.personal_descripcion,
                        nivel_prioridad=row.personal_prioridad,
                        es_procrastinacion=bool(row.personal_es_procrastinacion),
                        color=row.personal_color
                    )
                
                combined_site = CombinedSiteWithClassification(
                    id_sitio=row.id_sitio if row.tipo_sitio == 'base' else None,
                    dominio=row.dominio,
                    nombre=row.nombre,
                    tipo_sitio=row.tipo_sitio,
                    clasificacion_global=global_classification,
                    clasificacion_personal=personal_classification,
                    usando_clasificacion='personal' if personal_classification else 'global'
                )
                result.append(combined_site)
            
            return result
            
        except Exception as e:
            raise BusinessException(f"Error getting combined sites: {str(e)}")

    # CLASIFICACIONES DISPONIBLES
    async def get_all_classifications(self) -> List[ClassificationBase]:
        """Obtiene todas las clasificaciones disponibles"""
        try:
            classifications = await self.repository.get_all_classifications()
            return [ClassificationBase.model_validate(classification) for classification in classifications]
        except Exception as e:
            raise BusinessException(f"Error getting classifications: {str(e)}")

    # CLASIFICACIÓN UNIFICADA
    async def classify_site_unified(self, user_id: int, classification_data: UnifiedClassificationUpdate) -> ClassificationResponse:
        """Clasifica sitios base o personales automáticamente"""
        try:
            # Validar que la clasificación existe
            classifications = await self.repository.get_all_classifications()
            classification_ids = [c.id_clasificacion for c in classifications]
            if classification_data.id_clasificacion not in classification_ids:
                raise ValidationException(f"Classification with id {classification_data.id_clasificacion} does not exist")
            
            if classification_data.id_sitio:
                # 🏷️ Es sitio BASE
                site = await self.repository.get_site_base_by_id(classification_data.id_sitio)
                if not site:
                    raise NotFoundException(f"Site with id {classification_data.id_sitio} does not exist")
                
                from app.modules.sites.schemas.site_schema import UserClassificationCreate
                site_data = UserClassificationCreate(
                    id_sitio=classification_data.id_sitio,
                    id_clasificacion=classification_data.id_clasificacion
                )
                
                await self.repository.save_user_classification(site_data, user_id)
                return ClassificationResponse(
                    success=True,
                    message="Sitio base clasificado exitosamente",
                    tipo_sitio="base"
                )
                
            elif classification_data.dominio:
                # 🌟 Es sitio PERSONAL
                await self.repository.update_user_site_classification(
                    user_id, 
                    classification_data.dominio, 
                    classification_data.id_clasificacion
                )
                return ClassificationResponse(
                    success=True,
                    message="Sitio personal clasificado exitosamente", 
                    tipo_sitio="personal"
                )
            else:
                raise ValidationException("Must provide either id_sitio or dominio")
                
        except (ValidationException, NotFoundException):
            raise
        except Exception as e:
            raise BusinessException(f"Error classifying site: {str(e)}")

    # HISTORIAL DE NAVEGACIÓN
    async def start_navigation_session(self, user_id: int, history_data: NavigationHistoryCreate) -> int:
        """Inicia una sesión de navegación"""
        try:
            dominio = history_data.dominio
            
            # 1. Verificar si es sitio CURADO (Sitios_Base)
            site_base = await self.repository.get_site_base_by_domain(dominio)
            
            if site_base:
                # Sitio CURADO - usar Clasificacion_Usuario para preferencia personal
                user_classification = await self.repository.get_user_classification(user_id, site_base.id_sitio)
                classification_id = user_classification.id_clasificacion if user_classification else site_base.id_clasificacion
            else:
                # 2. Sitio NUEVO - usar Sitios_Usuario (personal, no compartido)
                user_site = await self.repository.get_or_create_user_site(user_id, dominio)
                classification_id = user_site.id_clasificacion
            
            # 3. Crear historial de navegación
            history = await self.repository.create_navigation_history(history_data, user_id, classification_id)
            return history.id_historial
            
        except Exception as e:
            raise BusinessException(f"Error starting navigation session: {str(e)}")

    async def end_navigation_session(self, history_id: int, update_data: NavigationHistoryUpdate) -> bool:
        """Finaliza una sesión de navegación"""
        try:
            updated = await self.repository.update_navigation_history(history_id, update_data)
            return updated is not None
        except Exception as e:
            raise BusinessException(f"Error ending navigation session: {str(e)}")
        
    async def update_site_classification(
        self, 
        user_id: int, 
        classification_data: SiteClassificationUpdate
    ) -> ClassificationResponse:
        """
        Actualiza la clasificación de un sitio (base o personal)
        """
        try:
            # Validar que la clasificación existe
            classifications = await self.repository.get_all_classifications()
            classification_ids = [c.id_clasificacion for c in classifications]
            if classification_data.id_clasificacion not in classification_ids:
                raise ValidationException(f"Classification with id {classification_data.id_clasificacion} does not exist")
            
            if classification_data.site_id:
                # 🏷️ Es sitio BASE
                site = await self.repository.get_site_base_by_id(classification_data.site_id)
                if not site:
                    raise NotFoundException(f"Site with id {classification_data.site_id} does not exist")
                
                from app.modules.sites.schemas.site_schema import UserClassificationCreate
                site_data = UserClassificationCreate(
                    id_sitio=classification_data.site_id,
                    id_clasificacion=classification_data.id_clasificacion
                )
                
                await self.repository.save_user_classification(site_data, user_id)
                return ClassificationResponse(
                    success=True,
                    message="Sitio base clasificado exitosamente",
                    tipo_sitio="base"
                )
                
            elif classification_data.dominio:
                # 🌟 Es sitio PERSONAL
                await self.repository.update_user_site_classification(
                    user_id, 
                    classification_data.dominio, 
                    classification_data.id_clasificacion
                )
                return ClassificationResponse(
                    success=True,
                    message="Sitio personal clasificado exitosamente", 
                    tipo_sitio="personal"
                )
            else:
                raise ValidationException("Must provide either site_id or dominio")
                
        except (ValidationException, NotFoundException):
            raise
        except Exception as e:
            raise BusinessException(f"Error updating site classification: {str(e)}")