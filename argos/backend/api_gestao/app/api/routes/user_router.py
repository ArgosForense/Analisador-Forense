from fastapi import APIRouter, Depends, Response
from typing import List
from beanie import PydanticObjectId
from app.api import dependencies
from app.schemas.user_schema import UserCreateSchema, UserResponseSchema
from app.controllers.user_controller import user_controller
from app.models.gestor_model import Gestor

router = APIRouter(
    prefix="/usuarios", 
    tags=["Usuários"], 
    dependencies=[Depends(dependencies.nivel_acesso_gestor)]
)

@router.get("/", response_model=List[UserResponseSchema])
async def listar_usuarios():
    """
    Lista todos os usuários e seus perfis.
    """
    return await user_controller.listar_usuarios()

@router.post("/", response_model=UserResponseSchema, status_code=201)
async def criar_usuario(
    user_in: UserCreateSchema,
    current_gestor: Gestor = Depends(dependencies.nivel_acesso_gestor)
):
    """
    Cria um novo usuário no sistema.
    
    - O gestor autenticado informa o nome, e-mail pessoal e perfil do novo usuário.
    - O sistema gera e envia as credenciais (e-mail institucional e senha) para o e-mail pessoal informado.
    - **Acesso:** Apenas Gestores.
    """
    return await user_controller.criar_novo_usuario(user_in=user_in, current_gestor=current_gestor)

@router.delete("/{user_id}", status_code=204)
async def deletar_usuario(user_id: PydanticObjectId):
    """
    Deleta um usuário permanentemente.
    """
    await user_controller.deletar_usuario(user_id=user_id)
    return Response(status_code=204)

@router.post("/{user_id}/ativar", response_model=UserResponseSchema)
async def ativar_usuario(user_id: PydanticObjectId):
    """
    Ativa a conta de um usuário que estava desativada.
    
    - Um usuário ativado pode fazer login no sistema.
    - **Acesso:** Apenas Gestores.
    """
    return await user_controller.ativar_usuario(user_id=user_id)

@router.post("/{user_id}/desativar", response_model=UserResponseSchema)
async def desativar_usuario(user_id: PydanticObjectId):
    """
    Desativa a conta de um usuário.
    
    - Um usuário desativado não pode mais fazer login no sistema.
    - **Acesso:** Apenas Gestores.
    """
    return await user_controller.desativar_usuario(user_id=user_id)