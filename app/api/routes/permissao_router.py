from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import dependencies
from app.schemas.permissao_schema import PermissaoCreateSchema, PermissaoResponseSchema
from app.controllers.permissao_controller import permissao_controller

router = APIRouter(
    prefix="/permissoes", 
    tags=["Permissões"], 
    dependencies=[Depends(dependencies.nivel_acesso_gestor)]
)

@router.post("/", response_model=PermissaoResponseSchema, status_code=201)
def create_permissao(
    *,
    permissao_in: PermissaoCreateSchema,
    db: Session = Depends(dependencies.get_db)
):
    """
    Cria uma nova permissão no sistema.
    - **Acesso:** Apenas Gestores.
    """
    return permissao_controller.create_new_permissao(db=db, permissao_in=permissao_in)