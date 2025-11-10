from app.core.exceptions import NotFoundException

from app.modules.users.implementation.user_repository import UserRepository
from app.modules.categories.implementation.category_website_repository import CategoryWebsiteRepository
from ..implementation.website_repository import WebsiteRepository
from ..implementation.website_user_repository import WebsiteUserRepository

from ..schemas.website_user_schema import (WebsiteUserCreate, WebsiteUserUpdate, WebsiteUserResponse, WebsiteUserListResponse)

class WebsiteUserService:
    def __init__(
            self,
            repo: WebsiteUserRepository,
            user_repo: UserRepository,
            website_repo: WebsiteRepository,
            category_repo: CategoryWebsiteRepository,
    ) -> None:
        self.repo = repo
        self.user_repo = user_repo
        self.website_repo = website_repo
        self.category_repo = category_repo

    async def create(self, data: WebsiteUserCreate) -> WebsiteUserResponse:
        user = await self.user_repo.get_by_id(data.id_usuarios)
        if user is None:
            raise NotFoundException("El ID de usuario proporcionado no existe.")

        website = await self.website_repo.get_by_id(data.id_sitios_web)
        if website is None:
            raise NotFoundException("El ID de sitio web proporcionado no existe.")

        category = await self.category_repo.get_by_id(data.id_categorias_web)
        if category is None:
            raise NotFoundException("El ID de categoría web proporcionado no existe.")

        registro = await self.repo.create(data)
        return WebsiteUserResponse.model_validate(registro)

    async def get_by_id(self, website_user_id: int) -> WebsiteUserResponse:
        registro = await self.repo.get_by_id(website_user_id)

        if registro is None:
            raise ValueError("No se encontró el registro solicitado.")

        return WebsiteUserResponse.model_validate(registro)

    async def get_by_user(self, user_id: int) -> list[WebsiteUserResponse]:
        registros = await self.repo.get_by_user(user_id)
        return [WebsiteUserResponse.model_validate(item) for item in registros]

    async def get_by_user_and_website(
        self, user_id: int, website_id: int
    ) -> WebsiteUserResponse:
        registro = await self.repo.get_by_user_and_website(user_id, website_id)
        return WebsiteUserResponse.model_validate(registro)

    async def get_by_user_and_category(
        self, user_id: int, category_id: int
    ) -> list[WebsiteUserResponse]:
        registros = await self.repo.get_by_user_and_category(user_id, category_id)
        return [WebsiteUserResponse.model_validate(item) for item in registros]

    async def update_by_user_and_website(
            self,
            user_id: int,
            website_id: int,
            data: WebsiteUserUpdate,
    ) -> WebsiteUserResponse:
        if data.id_categorias_web is not None:
            category = await self.category_repo.get_by_id(data.id_categorias_web)
            if category is None:
                raise NotFoundException("El ID de categoría web proporcionado no existe.")

        registro = await self.repo.update_by_user_and_website(user_id, website_id, data)
        return WebsiteUserResponse.model_validate(registro)
    
    async def get_user_website_list(
        self, user_id: int
    ) -> list[WebsiteUserListResponse]:
        
        sitios_globales = await self.website_repo.get_all_global()
        sitios_usuario = await self.repo.get_by_user(user_id)
        user_dict = {item.id_sitios_web for item in sitios_usuario}

        resultados: list[WebsiteUserListResponse] = []

        for sitio in sitios_globales:
            if sitio.id in user_dict:
                usuario_sitio = user_dict[sitio.id]
                category = await self.category_repo.get_by_id(usuario_sitio.id_categorias_web)
                category_name = category.nombre if category else "Desconocida"
            else:
                category = await self.category_repo.get_by_id(sitio.id)
                category_name = category.nombre if category else "Desconocida"
            website = await self.website_repo.get_by_id(sitio.id)
            dominio = website.dominio if website else "Desconocido"
            resultados.append(
                WebsiteUserListResponse(
                    id=sitio.id,
                    dominio=dominio,
                    categoria=category_name
                )
            )

        for item in sitios_usuario:
            if item.id_sitios_web not in [s.id_sitios_web for s in sitios_globales]:
                category = await self.category_repo.get_by_id(item.id_categorias_web)
                category_name = category.nombre if category else "Desconocida"

                website = await self.website_repo.get_by_id(item.id_sitios_web)
                dominio = website.dominio if website else "Desconocido"

                resultados.append(
                    WebsiteUserListResponse(
                        id=item.id_sitios_web,
                        dominio=dominio,
                        categoria=category_name
                    )
                )


        return resultados