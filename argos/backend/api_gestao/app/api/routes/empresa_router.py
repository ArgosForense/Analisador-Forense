from fastapi import APIRouter
from app.schemas.empresa_schema import EmpresaCreateSchema, EmpresaResponseSchema
from app.controllers.empresa_controller import empresa_controller

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.post("/cadastrar", response_model=EmpresaResponseSchema, status_code=201)
async def register_empresa(empresa_in: EmpresaCreateSchema):
    """
    Cadastra uma nova empresa no sistema.
    - Endpoint público para o cadastro inicial de empresas.
    """
    return await empresa_controller.create_new_empresa(empresa_in=empresa_in)