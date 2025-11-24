from fastapi import HTTPException, status
from typing import List
from beanie import PydanticObjectId
from app.models.permissao_model import Permissao
from app.models.perfil_model import Perfil
from app.schemas.permissao_schema import PermissaoCreateSchema, PermissaoUpdateSchema
from app.repositories.permissao_repository import permissao_repository

class PermissaoService:
    
    async def listar_permissoes(self) -> List[Permissao]:
        return await permissao_repository.get_all()

    async def criar_permissao(self, permissao_in: PermissaoCreateSchema):
        # Verifica duplicidade
        if await permissao_repository.get_by_name(nome=permissao_in.nome):
            raise HTTPException(status_code=400, detail="Permissão já existe")
        
        return await permissao_repository.create(obj_in=permissao_in)

    async def atualizar_permissao(self, permissao_id: PydanticObjectId, permissao_in: PermissaoUpdateSchema):
        permissao = await permissao_repository.get(permissao_id)
        if not permissao:
            raise HTTPException(status_code=404, detail="Permissão não encontrada")
        
        # Verifica se o novo nome já existe em OUTRA permissão
        permissao_com_nome = await permissao_repository.get_by_name(nome=permissao_in.nome)
        if permissao_com_nome and permissao_com_nome.id != permissao_id:
             raise HTTPException(status_code=400, detail="Já existe uma permissão com este nome")
        
        return await permissao_repository.update(id=permissao_id, obj_in=permissao_in)

    async def deletar_permissao(self, permissao_id: PydanticObjectId):
        permissao = await permissao_repository.get(permissao_id)
        if not permissao:
            raise HTTPException(status_code=404, detail="Permissão não encontrada")
            
        # --- CORREÇÃO AQUI ---
        # Verificação de segurança no MongoDB:
        # Buscamos Perfis que tenham esse ID na lista de permissões
        # O Beanie permite buscar dentro de listas de Links usando a sintaxe: campo.id
        uso = await Perfil.find(Perfil.permissoes.id == permissao.id).count()
        
        if uso > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Não é possível deletar. Esta permissão está em uso por {uso} perfil(is)."
            )
            
        await permissao_repository.remove(permissao_id)
        return True

permissao_service = PermissaoService()