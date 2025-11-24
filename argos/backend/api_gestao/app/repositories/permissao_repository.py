from typing import Optional
from .base_repository import BaseRepository
from app.models.permissao_model import Permissao
from app.schemas.permissao_schema import PermissaoCreateSchema, PermissaoUpdateSchema

class PermissaoRepository(BaseRepository[Permissao, PermissaoCreateSchema, PermissaoUpdateSchema]):
    
    async def get_by_name(self, nome: str) -> Optional[Permissao]:
        return await self.model.find_one(Permissao.nome == nome)

permissao_repository = PermissaoRepository(Permissao)