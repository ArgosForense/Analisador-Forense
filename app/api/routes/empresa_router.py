from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import dependencies
from app.schemas.empresa_schema import EmpresaCreateSchema, EmpresaResponseSchema
from app.controllers.empresa_controller import empresa_controller

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.post("/cadastrar", response_model=EmpresaResponseSchema, status_code=201)
def register_empresa(
    *,
    empresa_in: EmpresaCreateSchema,
    db: Session = Depends(dependencies.obter_sessao)
):
    """
    Cadastra uma nova empresa no sistema.
    - Endpoint público para o cadastro inicial de empresas.
    """
    return empresa_controller.create_new_empresa(db=db, empresa_in=empresa_in)