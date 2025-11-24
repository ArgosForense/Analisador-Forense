from typing import Optional
from .base_repository import BaseRepository
from app.models.gestor_model import Gestor
from app.schemas.gestor_schema import GestorCreateSchema

class GestorRepository(BaseRepository[Gestor, GestorCreateSchema, dict]):
    async def get_by_email(self, email: str) -> Optional[Gestor]:
        return await self.model.find_one(Gestor.email == email)

gestor_repository = GestorRepository(Gestor)