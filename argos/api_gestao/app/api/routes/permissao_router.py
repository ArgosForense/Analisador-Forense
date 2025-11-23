from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from typing import List
from app.api import dependencies
from app.schemas.permissao_schema import PermissaoCreateSchema, PermissaoResponseSchema, PermissaoUpdateSchema
from app.controllers.permissao_controller import permissao_controller

router = APIRouter(
    prefix="/permissoes", 
    tags=["Permissões"], 
    dependencies=[Depends(dependencies.nivel_acesso_gestor)]
)

@router.get("/", response_model=List[PermissaoResponseSchema])
def listar_permissoes(db: Session = Depends(dependencies.obter_sessao)):
    """
    Lista todas as permissões cadastradas.
    """
    return permissao_controller.listar_permissoes(db=db)

@router.post("/", response_model=PermissaoResponseSchema, status_code=201)
def criar_permissao(
    *,
    permissao_in: PermissaoCreateSchema,
    db: Session = Depends(dependencies.obter_sessao)
):
    """
    Cria uma nova permissão.
    """
    return permissao_controller.create_new_permissao(db=db, permissao_in=permissao_in)

@router.put("/{permissao_id}", response_model=PermissaoResponseSchema)
def atualizar_permissao(
    *,
    permissao_id: int,
    permissao_in: PermissaoUpdateSchema,
    db: Session = Depends(dependencies.obter_sessao)
):
    """
    Atualiza o nome de uma permissão existente.
    """
    return permissao_controller.update_permissao(db=db, permissao_id=permissao_id, permissao_in=permissao_in)

@router.delete("/{permissao_id}", status_code=204)
def deletar_permissao(
    *,
    permissao_id: int,
    db: Session = Depends(dependencies.obter_sessao)
):
    """
    Deleta uma permissão.
    - **Atenção:** Não é possível deletar se ela estiver vinculada a algum perfil.
    """
    permissao_controller.delete_permissao(db=db, permissao_id=permissao_id)
    return Response(status_code=204)