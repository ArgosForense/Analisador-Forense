from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api import dependencies
from app.schemas.perfil_schema import PerfilCreateSchema, PerfilResponseSchema
from app.controllers.perfil_controller import perfil_controller

router = APIRouter(
    prefix="/perfis", 
    tags=["Perfis"], 
    dependencies=[Depends(dependencies.nivel_acesso_gestor)]
)

@router.get("/", response_model=List[PerfilResponseSchema])
def ler_perfis(
    db: Session = Depends(dependencies.obter_sessao)
):
    """
    Lista todos os perfis disponíveis no sistema.
    - Usado para preencher o select de cadastro de usuários.
    - **Acesso:** Apenas Gestores.
    """
    return perfil_controller.listar_todos_perfis(db=db)

@router.post("/", response_model=PerfilResponseSchema, status_code=201)
def criar_perfil(
    *,
    perfil_in: PerfilCreateSchema,
    db: Session = Depends(dependencies.obter_sessao)
):
    """
    Cria um novo perfil com um conjunto de permissões.
    - **Acesso:** Apenas Gestores.
    """
    return perfil_controller.create_new_perfil(db=db, perfil_in=perfil_in)

@router.delete("/{perfil_id}", status_code=204)
def deletar_perfil(
    *,
    perfil_id: int,
    db: Session = Depends(dependencies.obter_sessao)
):
    """
    Deleta um perfil existente.
    - Não permite deletar se houver usuários associados.
    - **Acesso:** Apenas Gestores.
    """