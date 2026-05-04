from ..implementation.intervention_repository import InterventionRepository
from ..schemas.intervention_schema import (
    IntAvisoCreate,
    IntAvisoResponse,
    IntBloqueoCreate,
    IntBloqueoResponse,
    IntEscrituraCreate,
    IntEscrituraResponse,
    InterventionCreate,
    InterventionResponse,
    InterventionUpdateUnlockDate,
)


class InterventionService:
    def __init__(self, repo: InterventionRepository) -> None:
        self.repo = repo

    async def create_intervention(self, data: InterventionCreate) -> InterventionResponse:
        registro = await self.repo.create_intervention(data)
        return InterventionResponse.model_validate(registro)

    async def get_intervention_by_id(self, intervention_id: int) -> InterventionResponse:
        registro = await self.repo.get_intervention_by_id(intervention_id)
        if registro is None:
            raise ValueError("No se encontró la intervención con el id especificado.")
        return InterventionResponse.model_validate(registro)

    async def get_today_count_by_user(self, user_id: int) -> int:
        return await self.repo.get_today_count_by_user(user_id)

    async def get_last_by_user_if_today(self, user_id: int) -> InterventionResponse | None:
        registro = await self.repo.get_last_by_user_if_today(user_id)
        if registro is None:
            return None
        return InterventionResponse.model_validate(registro)

    async def get_interventions_by_user(self, user_id: int) -> list[InterventionResponse]:
        registros = await self.repo.get_interventions_by_user(user_id)
        return [InterventionResponse.model_validate(item) for item in registros]

    async def update_unlock_date(
        self,
        intervention_id: int,
        data: InterventionUpdateUnlockDate,
    ) -> InterventionResponse:
        registro = await self.repo.update_unlock_date(intervention_id, data)
        if registro is None:
            raise ValueError("No se encontró la intervención con el id especificado.")
        return InterventionResponse.model_validate(registro)

    async def delete_intervention_by_id(self, intervention_id: int) -> None:
        eliminado = await self.repo.delete_intervention_by_id(intervention_id)
        if not eliminado:
            raise ValueError("No se encontró la intervención con el id especificado.")

    async def create_int_aviso(self, data: IntAvisoCreate) -> IntAvisoResponse:
        registro = await self.repo.create_int_aviso(data)
        return IntAvisoResponse.model_validate(registro)

    async def delete_int_aviso_by_pk(self, intervention_id: int) -> None:
        eliminado = await self.repo.delete_int_aviso_by_pk(intervention_id)
        if not eliminado:
            raise ValueError("No se encontró el aviso con la primary key especificada.")

    async def create_int_bloqueo(self, data: IntBloqueoCreate) -> IntBloqueoResponse:
        registro = await self.repo.create_int_bloqueo(data)
        return IntBloqueoResponse.model_validate(registro)

    async def delete_int_bloqueo_by_pk(self, intervention_id: int) -> None:
        eliminado = await self.repo.delete_int_bloqueo_by_pk(intervention_id)
        if not eliminado:
            raise ValueError("No se encontró el bloqueo con la primary key especificada.")

    async def create_int_escritura(self, data: IntEscrituraCreate) -> IntEscrituraResponse:
        registro = await self.repo.create_int_escritura(data)
        return IntEscrituraResponse.model_validate(registro)

    async def delete_int_escritura_by_pk(self, intervention_id: int) -> None:
        eliminado = await self.repo.delete_int_escritura_by_pk(intervention_id)
        if not eliminado:
            raise ValueError("No se encontró la escritura con la primary key especificada.")
