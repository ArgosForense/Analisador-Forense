from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import dependencies
from app.schemas.user_schema import UserCreateSchema, UserResponseSchema
from app.controllers.user_controller import user_controller
from app.models.gestor_model import Gestor



# A dependência de nivel_acesso_gestor pode ser aplicada a todo o router para evitar repetição em cada rota.
router = APIRouter(
    prefix="/usuarios", 
    tags=["Usuários"], 
    dependencies=[Depends(dependencies.nivel_acesso_gestor)]
)

@router.post("/", response_model=UserResponseSchema, status_code=201)
def criar_usuario(
    *,
    user_in: UserCreateSchema,
    db: Session = Depends(dependencies.obter_sessao),
    
    # A dependência nivel_acesso_gestor já garante que o usuário é um gestor e o retorna, então podemos usá-lo diretamente.
    current_gestor: Gestor = Depends(dependencies.nivel_acesso_gestor)
):
    """
    Cria um novo usuário no sistema.
    
    - O gestor autenticado informa o nome, e-mail pessoal e perfil do novo usuário.
    - O sistema gera e envia as credenciais (e-mail institucional e senha) para o e-mail pessoal informado.
    - **Acesso:** Apenas Gestores.
    """
    return user_controller.criar_novo_usuario(db=db, user_in=user_in, current_gestor=current_gestor)

@router.post("/{user_id}/ativar", response_model=UserResponseSchema)
def ativar_usuario(
    *,
    user_id: int,
    db: Session = Depends(dependencies.obter_sessao)
):
    """
    Ativa a conta de um usuário que estava desativada.
    
    - Um usuário ativado pode fazer login no sistema.
    - **Acesso:** Apenas Gestores.
    """
    return user_controller.ativar_usuario(db=db, user_id=user_id)

@router.post("/{user_id}/desativar", response_model=UserResponseSchema)
def desativar_usuario(
    *,
    user_id: int,
    db: Session = Depends(dependencies.obter_sessao)
):
    """
    Desativa a conta de um usuário.
    
    - Um usuário desativado não pode mais fazer login no sistema.
    - **Acesso:** Apenas Gestores.
    """
    return user_controller.desativar_usuario(db=db, user_id=user_id)