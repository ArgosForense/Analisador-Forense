from fastapi import APIRouter, Depends, Response
from typing import List
from beanie import PydanticObjectId
from app.api import dependencies
from app.schemas.permissao_schema import PermissaoCreateSchema, PermissaoResponseSchema, PermissaoUpdateSchema
from app.controllers.permissao_controller import permissao_controller

router = APIRouter(
    prefix="/permissoes", 
    tags=["Permissões"], 
    dependencies=[Depends(dependencies.nivel_acesso_gestor)]
)

@router.get("/", response_model=List[PermissaoResponseSchema])
async def listar_permissoes():
    """
    Lista todas as permissões cadastradas.
    """
    return await permissao_controller.listar_permissoes()

@router.post("/", response_model=PermissaoResponseSchema, status_code=201)
async def criar_permissao(permissao_in: PermissaoCreateSchema):
    """
    Cria uma nova permissão.
    """
    return await permissao_controller.create_new_permissao(permissao_in=permissao_in)

@router.put("/{permissao_id}", response_model=PermissaoResponseSchema)
async def atualizar_permissao(permissao_id: PydanticObjectId, permissao_in: PermissaoUpdateSchema):
    """
    Atualiza o nome de uma permissão existente.
    """
    return await permissao_controller.update_permissao(permissao_id=permissao_id, permissao_in=permissao_in)

@router.delete("/{permissao_id}", status_code=204)
async def deletar_permissao(permissao_id: PydanticObjectId):
    """
    Deleta uma permissão.
    - **Atenção:** Não é possível deletar se ela estiver vinculada a algum perfil.
    """
    await permissao_controller.delete_permissao(permissao_id=permissao_id)
    return Response(status_code=204)