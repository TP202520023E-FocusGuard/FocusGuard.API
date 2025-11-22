from app.core.exceptions import NotFoundException

from app.modules.users.implementation.user_repository import UserRepository

from ..implementation.content_user_repository import ContentUserRepository
from ..implementation.content_visited_repository import ContentVisitedRepository
from ..schemas.content_visited_schema import ContentVisitedCreate, ContentVisitedResponse


class ContentVisitedService:
    def __init__(
        self,
        repo: ContentVisitedRepository,
        user_repo: UserRepository,
        content_user_repo: ContentUserRepository,
    ) -> None:
        self.repo = repo
        self.user_repo = user_repo
        self.content_user_repo = content_user_repo

    async def create(self, data: ContentVisitedCreate) -> ContentVisitedResponse:
        user = await self.user_repo.get_by_id(data.id_usuarios)
        if user is None:
            raise NotFoundException("El ID de usuario proporcionado no existe.")

        content_user = await self.content_user_repo.get_by_id(data.id_contenidos_usuario)
        if content_user is None:
            raise NotFoundException(
                "El ID de contenido de usuario proporcionado no existe."
            )

        if content_user.id_usuarios != data.id_usuarios:
            raise ValueError(
                "El usuario proporcionado no coincide con el usuario del contenido."
            )

        registro = await self.repo.create(data)
        return ContentVisitedResponse.model_validate(registro)

    async def get_all(self) -> list[ContentVisitedResponse]:
        registros = await self.repo.get_all()
        return [ContentVisitedResponse.model_validate(item) for item in registros]

    async def get_by_id(self, record_id: int) -> ContentVisitedResponse:
        registro = await self.repo.get_by_id(record_id)

        if registro is None:
            raise ValueError("No se encontró el registro solicitado.")

        return ContentVisitedResponse.model_validate(registro)

    async def get_by_user(self, user_id: int) -> list[ContentVisitedResponse]:
        registros = await self.repo.get_by_user(user_id)
        return [ContentVisitedResponse.model_validate(item) for item in registros]

    async def get_by_user_and_content_user(
        self, user_id: int, content_user_id: int
    ) -> list[ContentVisitedResponse]:
        registros = await self.repo.get_by_user_and_content_user(user_id, content_user_id)
        return [ContentVisitedResponse.model_validate(item) for item in registros]

    async def delete_by_id(self, record_id: int) -> None:
        eliminado = await self.repo.delete_by_id(record_id)

        if not eliminado:
            raise ValueError("No se encontró el registro solicitado.")