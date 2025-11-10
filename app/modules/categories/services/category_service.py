from typing import List
from app.modules.categories.schemas.category_schema import ChangeCategory, ChangeCategoryCreate
from app.modules.categories.implementation.category_repository import CategoryRepository
from app.modules.websites.services.website_user_service import WebsiteUserService
from app.modules.websites.schemas.website_user_schema import WebsiteUserUpdate
from datetime import datetime
class ChangeCategoryService:
    def __init__(self, repo: CategoryRepository, website_user_service: WebsiteUserService):
        self.repo = repo
        self.website_user_service = website_user_service
    
    async def get_all(self) -> List[ChangeCategory]:
        cambios = await self.repo.get_all()
        return [ChangeCategory.model_validate(c) for c in cambios]
    
    async def get_by_id(self, change_id: int) -> ChangeCategory:
        cambio = await self.repo.get_by_id(change_id)
        if not cambio:
            raise ValueError("Cambio de categoría no encontrado")
        return ChangeCategory.model_validate(cambio)
    
    async def create(self, data: ChangeCategoryCreate) -> ChangeCategory:
        user_website = await self.website_user_service.get_by_id(data.id_sitios_web_usuario)
        if not user_website:
            raise ValueError("Sitio web del usuario no encontrado")

        categoria_anterior = user_website.id_categorias_web

        cambio = await self.repo.create({
            "id_usuarios": data.id_usuarios,
            "id_sitios_web_usuario": data.id_sitios_web_usuario,
            "id_categorias_web_anterior": categoria_anterior,
            "id_categorias_web_nuevo": data.id_categorias_web_nuevo,
            "fecha_hora": datetime.utcnow()
        })

        update_data = WebsiteUserUpdate(id_categorias_web=data.id_categorias_web_nuevo)
        await self.website_user_service.update_by_user_and_website(
            user_id=data.id_usuarios,
            website_id=user_website.id_sitios_web,
            data=update_data
        )

        return ChangeCategory.model_validate(cambio)