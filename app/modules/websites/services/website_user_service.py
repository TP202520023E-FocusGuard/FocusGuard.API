from __future__ import annotations

from ..implementation.website_user_repository import WebsiteUserRepository
from ..schemas.website_user_schema import (WebsiteUserCreate, WebsiteUserUpdate, WebsiteUserResponse)


class WebsiteUserService:
    def __init__(self, repo: WebsiteUserRepository) -> None:
        self.repo = repo

    def create(self, data: WebsiteUserCreate) -> WebsiteUserResponse:
        registro = self.repo.create(data)
        return WebsiteUserResponse.model_validate(registro)

    def get_by_user(self, user_id: int) -> list[WebsiteUserResponse]:
        registros = self.repo.get_by_user(user_id)
        return [WebsiteUserResponse.model_validate(item) for item in registros]

    def get_by_user_and_website(
        self, user_id: int, website_id: int
    ) -> WebsiteUserResponse:
        registro = self.repo.get_by_user_and_website(user_id, website_id)
        return WebsiteUserResponse.model_validate(registro)

    def get_by_user_and_category(
        self, user_id: int, category_id: int
    ) -> list[WebsiteUserResponse]:
        registros = self.repo.get_by_user_and_category(user_id, category_id)
        return [WebsiteUserResponse.model_validate(item) for item in registros]

    def update_by_user_and_website(
            self,
            user_id: int,
            website_id: int,
            data: WebsiteUserUpdate,
    ) -> WebsiteUserResponse:
        registro = self.repo.update_by_user_and_website(user_id, website_id, data)
        return WebsiteUserResponse.model_validate(registro)