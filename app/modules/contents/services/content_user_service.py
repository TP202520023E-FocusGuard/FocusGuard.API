from app.core.exceptions import NotFoundException

from app.modules.users.implementation.user_repository import UserRepository
from app.modules.websites.implementation.website_user_repository import WebsiteUserRepository
from app.modules.categories.implementation.category_content_repository import CategoryContentRepository
from ..implementation.content_repository import ContentRepository
from ..implementation.content_user_repository import ContentUserRepository

from ..schemas.content_user_schema import ContentUserCreate, ContentUserUpdate, ContentUserResponse


class ContentUserService:
    def __init__(
            self,
            repo: ContentUserRepository,
            user_repo=UserRepository,
            content_repo=ContentRepository,
            category_content_repo=CategoryContentRepository,
            website_user_repo=WebsiteUserRepository
    ) -> None:
        self.repo = repo
        self.user_repo = user_repo
        self.content_repo = content_repo
        self.category_content_repo = category_content_repo
        self.website_user_repo = website_user_repo

    async def create(self, data: ContentUserCreate) -> ContentUserResponse:

        existed_content_user = await self.repo.get_by_user_site_and_content(data.id_usuarios, data.id_sitios_web_usuario, data.id_contenidos)

        if existed_content_user is not None:
            return ContentUserResponse.model_validate(existed_content_user)

        user = await self.user_repo.get_by_id(data.id_usuarios)
        if user is None:
            raise NotFoundException("El ID de usuario proporcionado no existe.")

        content = await self.content_repo.get_by_id(data.id_contenidos)
        if content is None:
            raise NotFoundException("El ID de contenido proporcionado no existe.")

        category_content = await self.category_content_repo.get_by_id(data.id_categorias_contenido)
        if category_content is None:
            raise NotFoundException("El ID de categoría de contenido proporcionado no existe.")

        website_user = await self.website_user_repo.get_by_id(data.id_sitios_web_usuario)
        if website_user is None:
            raise NotFoundException("El ID de sitioweb-usuario proporcionado no existe.")
        if website_user.id_usuarios != data.id_usuarios:
            raise ValueError("El usuario que está ingresando no coincide con el usuario del sitio web.")

        registro = await self.repo.create(data)
        return ContentUserResponse.model_validate(registro)

    async def get_all(self) -> list[ContentUserResponse]:
        registros = await self.repo.get_all()
        return [ContentUserResponse.model_validate(item) for item in registros]

    async def get_by_id(self, record_id: int) -> ContentUserResponse:
        registro = await self.repo.get_by_id(record_id)

        if registro is None:
            raise ValueError("No se encontró un registro con el id especificado.")

        return ContentUserResponse.model_validate(registro)

    async def get_by_user(self, user_id: int) -> list[ContentUserResponse]:
        registros = await self.repo.get_by_user(user_id)
        return [ContentUserResponse.model_validate(item) for item in registros]

    async def get_by_user_and_site(
        self, user_id: int, site_id: int
    ) -> list[ContentUserResponse]:
        registros = await self.repo.get_by_user_and_site(user_id, site_id)
        return [ContentUserResponse.model_validate(item) for item in registros]

    # async def get_by_user_site_and_content(
    #     self, user_id: int, site_id: int, content_id: int
    # ) -> list[ContentUserResponse]:
    #     registros = await self.repo.get_by_user_site_and_content(
    #         user_id, site_id, content_id
    #     )
    #     return [ContentUserResponse.model_validate(item) for item in registros]

    async def get_by_user_site_and_content(
        self, user_id: int, site_id: int, content_id: int
    ) -> ContentUserResponse:
        registro = await self.repo.get_by_user_site_and_content(
            user_id, site_id, content_id
        )
        return ContentUserResponse.model_validate(registro)

    async def get_by_user_and_category(
        self, user_id: int, category_id: int
    ) -> list[ContentUserResponse]:
        registros = await self.repo.get_by_user_and_category(user_id, category_id)
        return [ContentUserResponse.model_validate(item) for item in registros]

    async def update_by_id(
            self,
            content_user_id: int,
            data: ContentUserUpdate,
    ) -> ContentUserResponse:
        if data.id_categorias_contenido is not None:
            category = await self.category_content_repo.get_by_id(data.id_categorias_contenido)
            if category is None:
                raise NotFoundException("El ID de categoría de contenido proporcionado no existe.")

        registro = await self.repo.update_by_id(content_user_id, data)
        return ContentUserResponse.model_validate(registro)

    async def delete_by_id(self, record_id: int) -> None:
        eliminado = await self.repo.delete_by_id(record_id)

        if not eliminado:
            raise ValueError("No se encontró un registro con el id especificado.")