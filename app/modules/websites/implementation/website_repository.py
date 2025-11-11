from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.website_model import WebsiteModel, WebsiteglobalModel
from ..schemas.website_schema import WebsiteCreate, WebsiteGlobalResponse

class WebsiteRepository:

    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(self, data: WebsiteCreate) -> WebsiteModel:
        nuevo_website = WebsiteModel(
            dominio=data.dominio,
        )

        try:
            self.db.add(nuevo_website)
            await self.db.commit()
            await self.db.refresh(nuevo_website)
            return nuevo_website
        except IntegrityError as exc:
            await self.db.rollback()
            raise ValueError("El dominio ya se encuentra registrado.") from exc
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_all(self) -> list[WebsiteModel]:
        registros = await self.db.scalars(select(WebsiteModel))
        return list(registros.all())

    async def get_all_global(self) -> list[WebsiteglobalModel]:
        registros = await self.db.scalars(select(WebsiteglobalModel))
        return list(registros.all())

    async def get_by_id(self, website_id: int) -> Optional[WebsiteModel]:
        return await self.db.get(WebsiteModel, website_id)

    async def get_by_domain(self, domain: str) -> Optional[WebsiteModel]:
        stmt = select(WebsiteModel).where(WebsiteModel.dominio == domain)
        return (await self.db.scalars(stmt)).one_or_none()

    async def delete(self, registro: WebsiteModel) -> None:
        try:
            await self.db.delete(registro)
            await self.db.commit()
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def delete_by_id(self, website_id: int) -> bool:
        registro = await self.get_by_id(website_id)

        if registro is None:
            return False

        await self.delete(registro)
        return True

    async def delete_by_domain(self, domain: str) -> bool:
        registro = await self.get_by_domain(domain)

        if registro is None:
            return False

        await self.delete(registro)
        return True