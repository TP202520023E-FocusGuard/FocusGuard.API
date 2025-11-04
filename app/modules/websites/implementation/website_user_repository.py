from __future__ import annotations
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from ..models.website_user_model import WebsiteUserModel
from ..schemas.website_user_schema import WebsiteUserCreate


class WebsiteUserRepository:
    def __init__(self, db_session: Session) -> None:
        self.db = db_session

    def create(self, data: WebsiteUserCreate) -> WebsiteUserModel:
        registro = WebsiteUserModel(
            id_usuarios=data.id_usuarios,
            id_sitios_web=data.id_sitios_web,
            id_categorias_web=data.id_categorias_web,
            origen=data.origen or "custom",
        )

        try:
            self.db.add(registro)
            self.db.commit()
            self.db.refresh(registro)
            return registro
        except IntegrityError as exc:
            self.db.rollback()
            raise ValueError(
                "Ya existe un registro para este usuario y sitio web."
            ) from exc
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_by_user(self, user_id: int) -> list[WebsiteUserModel]:

        stmt = select(WebsiteUserModel).where(
            WebsiteUserModel.id_usuarios == user_id
        )
        registros = self.db.scalars(stmt).all()

        return list(registros)

    def get_by_user_and_website(
            self, user_id: int, website_id: int
    ) -> Optional[WebsiteUserModel]:

        stmt = select(WebsiteUserModel).where(
            WebsiteUserModel.id_usuarios == user_id,
            WebsiteUserModel.id_sitios_web == website_id
        )

        return self.db.scalars(stmt).one_or_none()

    def get_by_user_and_category(
            self, user_id: int, category_id: int
    ) -> list[WebsiteUserModel]:

        stmt = select(WebsiteUserModel).where(
            WebsiteUserModel.id_usuarios == user_id,
            WebsiteUserModel.id_categorias_web == category_id
        )

        registros = self.db.scalars(stmt).all()

        return list(registros)