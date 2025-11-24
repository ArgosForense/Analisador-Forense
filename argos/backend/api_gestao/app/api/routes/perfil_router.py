from fastapi import APIRouter, Depends, Response
from typing import List
from beanie import PydanticObjectId
from app.api import dependencies
from app.schemas.perfil_schema import PerfilCreateSchema, PerfilResponseSchema
from app.controllers.perfil_controller import perfil_controller

router = APIRouter(
    prefix="/perfis", 
    tags=["Perfis"], 
    dependencies=[Depends(dependencies.nivel_acesso_gestor)]
)

@router.get("/", response_model=List[PerfilResponseSchema])
async def ler_perfis():
    """
    Lista todos os perfis disponíveis no sistema.
    - Usado para preencher o select de cadastro de usuários.
    - **Acesso:** Apenas Gestores.
    """
    return await perfil_controller.listar_todos_perfis()

@router.post("/", response_model=PerfilResponseSchema, status_code=201)
async def criar_perfil(perfil_in: PerfilCreateSchema):
    """
    Cria um novo perfil com um conjunto de permissões.
    - **Acesso:** Apenas Gestores.
    """
    return await perfil_controller.create_new_perfil(perfil_in=perfil_in)

@router.delete("/{perfil_id}", status_code=204)
async def deletar_perfil(perfil_id: PydanticObjectId):
    """
    Deleta um perfil existente.
    - Não permite deletar se houver usuários associados.
    - **Acesso:** Apenas Gestores.
    """
    await perfil_controller.delete_perfil(perfil_id=perfil_id)
    return Response(status_code=204)