from app.core.exceptions import NotFoundException

from app.modules.users.implementation.user_repository import UserRepository
from app.modules.categories.implementation.category_website_repository import CategoryWebsiteRepository
from ..implementation.website_repository import WebsiteRepository

from ..implementation.website_user_repository import WebsiteUserRepository
from ..schemas.website_user_schema import (WebsiteUserCreate, WebsiteUserUpdate, WebsiteUserResponse)


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