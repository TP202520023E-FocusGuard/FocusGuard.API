from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.intervention_model import (
    IntAvisoModel,
    IntBloqueoModel,
    IntEscrituraModel,
    InterventionModel,
)
from ..schemas.intervention_schema import (
    IntAvisoCreate,
    IntBloqueoCreate,
    IntEscrituraCreate,
    InterventionCreate,
    InterventionUpdateUnlockDate,
)


class InterventionRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create_intervention(self, data: InterventionCreate) -> InterventionModel:
        registro = InterventionModel(**data.model_dump())
        try:
            self.db.add(registro)
            await self.db.commit()
            await self.db.refresh(registro)
            return registro
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_intervention_by_id(self, intervention_id: int) -> Optional[InterventionModel]:
        return await self.db.get(InterventionModel, intervention_id)

    async def get_interventions_by_user(self, user_id: int) -> list[InterventionModel]:
        stmt = (
            select(InterventionModel)
            .where(InterventionModel.id_usuarios == user_id)
            .order_by(InterventionModel.fecha_despliegue.desc())
        )
        registros = await self.db.scalars(stmt)
        return list(registros.all())

    async def get_today_count_by_user(self, user_id: int) -> int:
        stmt = select(func.count(InterventionModel.id)).where(
            InterventionModel.id_usuarios == user_id,
            func.date(InterventionModel.fecha_despliegue) == datetime.now().date(),
        )
        return int((await self.db.scalar(stmt)) or 0)

    async def get_last_by_user_if_today(self, user_id: int) -> Optional[InterventionModel]:
        stmt = (
            select(InterventionModel)
            .where(InterventionModel.id_usuarios == user_id)
            .order_by(InterventionModel.fecha_despliegue.desc())
            .limit(1)
        )
        registro = (await self.db.execute(stmt)).scalar_one_or_none()

        if registro is None:
            return None

        if registro.fecha_despliegue.date() != datetime.now().date():
            return None

        return registro

    async def update_unlock_date(
        self,
        intervention_id: int,
        data: InterventionUpdateUnlockDate,
    ) -> Optional[InterventionModel]:
        registro = await self.get_intervention_by_id(intervention_id)

        if registro is None:
            return None

        try:
            registro.fecha_desbloqueo = data.fecha_desbloqueo
            await self.db.commit()
            await self.db.refresh(registro)
            return registro
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def delete_intervention_by_id(self, intervention_id: int) -> bool:
        registro = await self.get_intervention_by_id(intervention_id)

        if registro is None:
            return False

        try:
            await self.db.delete(registro)
            await self.db.commit()
            return True
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def create_int_aviso(self, data: IntAvisoCreate) -> IntAvisoModel:
        registro = IntAvisoModel(**data.model_dump())
        self.db.add(registro)
        await self.db.commit()
        await self.db.refresh(registro)
        return registro

    async def delete_int_aviso_by_pk(self, intervention_id: int) -> bool:
        registro = await self.db.get(IntAvisoModel, intervention_id)
        if registro is None:
            return False
        await self.db.delete(registro)
        await self.db.commit()
        return True

    async def create_int_bloqueo(self, data: IntBloqueoCreate) -> IntBloqueoModel:
        registro = IntBloqueoModel(**data.model_dump())
        self.db.add(registro)
        await self.db.commit()
        await self.db.refresh(registro)
        return registro

    async def delete_int_bloqueo_by_pk(self, intervention_id: int) -> bool:
        registro = await self.db.get(IntBloqueoModel, intervention_id)
        if registro is None:
            return False
        await self.db.delete(registro)
        await self.db.commit()
        return True

    async def create_int_escritura(self, data: IntEscrituraCreate) -> IntEscrituraModel:
        registro = IntEscrituraModel(**data.model_dump())
        self.db.add(registro)
        await self.db.commit()
        await self.db.refresh(registro)
        return registro

    async def delete_int_escritura_by_pk(self, intervention_id: int) -> bool:
        registro = await self.db.get(IntEscrituraModel, intervention_id)
        if registro is None:
            return False
        await self.db.delete(registro)
        await self.db.commit()
        return True
