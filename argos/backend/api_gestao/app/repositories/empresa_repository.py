from typing import Optional
from .base_repository import BaseRepository
from app.models.empresa_model import Empresa
from app.schemas.empresa_schema import EmpresaCreateSchema

class EmpresaRepository(BaseRepository[Empresa, EmpresaCreateSchema, dict]):
    async def get_by_cnpj(self, cnpj: str) -> Optional[Empresa]:
        return await self.model.find_one(Empresa.cnpj == cnpj)

empresa_repository = EmpresaRepository(Empresa)