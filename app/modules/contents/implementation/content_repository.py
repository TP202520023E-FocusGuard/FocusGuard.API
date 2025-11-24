from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.content_model import ContentModel
from ..schemas.content_schema import ContentCreate


class ContentRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(self, data: ContentCreate) -> ContentModel:
        nuevo_contenido = ContentModel(
            titulo=data.titulo,
            descripcion=data.descripcion,
            twitter_cards=data.twitter_cards,
        )

        try:
            self.db.add(nuevo_contenido)
            await self.db.commit()
            await self.db.refresh(nuevo_contenido)
            return nuevo_contenido
        except IntegrityError as exc:
            await self.db.rollback()
            raise ValueError("El titulo del contenido ya se encuentra registrado.") from exc
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_all(self) -> list[ContentModel]:
        registros = await self.db.scalars(select(ContentModel))
        return list(registros.all())

    async def get_by_id(self, content_id: int) -> Optional[ContentModel]:
        return await self.db.get(ContentModel, content_id)

    async def get_by_title(self, title: str) -> Optional[ContentModel]:
        stmt = select(ContentModel).where(ContentModel.titulo == title)
        return (await self.db.scalars(stmt)).one_or_none()

    async def delete(self, registro: ContentModel) -> None:
        try:
            await self.db.delete(registro)
            await self.db.commit()
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def delete_by_id(self, content_id: int) -> bool:
        registro = await self.get_by_id(content_id)

        if registro is None:
            return False

        await self.delete(registro)
        return True