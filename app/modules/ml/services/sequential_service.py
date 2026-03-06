from app.core.exceptions import NotFoundException
from ..implementation.sequential_repository import MLSequentialRepository
from ..schemas.sequential_schema import MLInputPayload, MLInputItem

class MLService:
    def __init__(self, repo: MLSequentialRepository) -> None:
        self.repo = repo

    async def get_last_10_for_ml(self, user_id: int) -> MLInputPayload:
        """
        Retorna los últimos 10 registros del usuario listos para enviarse al ML,
        incluyendo solo la categoría y el tiempo de estancia.
        """
        visitados = await self.repo.get_last_10_for_ml(user_id)

        if not visitados:
            raise NotFoundException(f"No se encontraron registros para el usuario {user_id}")
        items = [MLInputItem(**v) for v in visitados]

        return MLInputPayload(
            user_id=user_id, 
            registros=items
        )