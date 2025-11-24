from fastapi import HTTPException, status
from typing import List
from beanie import PydanticObjectId
from app.models.perfil_model import Perfil
from app.models.permissao_model import Permissao
from app.models.user_model import Usuario
from app.schemas.perfil_schema import PerfilCreateSchema
from app.repositories.perfil_respository import perfil_repository

class PerfilService:
    
    async def listar_perfis(self) -> List[Perfil]:
        return await perfil_repository.get_all()
    
    async def criar_perfil(self, perfil_in: PerfilCreateSchema) -> Perfil:
        # Busca as permissões pelos IDs recebidos
        # O operador $in busca documentos onde o _id está na lista fornecida
        permissoes_encontradas = await Permissao.find(
            {"_id": {"$in": perfil_in.permissoes_ids}}
        ).to_list()
        
        if len(permissoes_encontradas) != len(perfil_in.permissoes_ids):
            raise HTTPException(status_code=400, detail="Uma ou mais permissões não foram encontradas.")
            
        # Cria o perfil linkando os objetos de permissão encontrados
        perfil = Perfil(nome=perfil_in.nome, permissoes=permissoes_encontradas)
        await perfil.create()
        return perfil
        
    async def deletar_perfil(self, perfil_id: PydanticObjectId):
        perfil = await perfil_repository.get(perfil_id)
        if not perfil:
            raise HTTPException(status_code=404, detail="Perfil não encontrado.")

        # Verifica se há usuários vinculados a este perfil
        # No Beanie, buscamos pelo campo de link (Usuario.perfil.id)
        usuarios_vinculados = await Usuario.find(Usuario.perfil.id == perfil.id).count()
        
        if usuarios_vinculados > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Não é possível excluir. Existem {usuarios_vinculados} usuário(s) vinculados a este perfil."
            )
        
        await perfil.delete()
        return True

perfil_service = PerfilService()