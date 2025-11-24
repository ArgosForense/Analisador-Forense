from typing import Optional, List
from beanie import PydanticObjectId
from .base_repository import BaseRepository
from app.models.perfil_model import Perfil
from app.models.permissao_model import Permissao
from app.schemas.perfil_schema import PerfilCreateSchema

class PerfilRepository(BaseRepository[Perfil, PerfilCreateSchema, dict]):
    async def get_by_name(self, nome: str) -> Optional[Perfil]:
        """
        Busca um perfil pelo nome.
        """
        return await self.model.find_one(Perfil.nome == nome)
    
    async def create_with_permissions(self, nome: str, permissoes: List[Permissao]) -> Perfil:
        """
        Cria um novo objeto Perfil no banco de dados, já associando as permissões.
        """
        # No Mongo, salvamos a lista de objetos (Links)
        # O Beanie extrai os IDs automaticamente
        perfil = Perfil(nome=nome, permissoes=permissoes)
        await perfil.create()
        return perfil

# Inicializar passando o Modelo (Perfil) para o construtor do Pai (BaseRepository)
perfil_repository = PerfilRepository(Perfil)