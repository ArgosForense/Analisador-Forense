from fastapi import APIRouter
from app.schemas.gestor_schema import GestorCreateSchema, GestorResponseSchema
from app.controllers.gestor_controller import gestor_controller

router = APIRouter(prefix="/gestores", tags=["Gestores"])

# Rota pública para criar o primeiro gestor
@router.post("/criar_conta", response_model=GestorResponseSchema, status_code=201)
async def create_account(gestor_in: GestorCreateSchema):
    """
    Cria uma nova conta de gestor, vinculada a uma empresa existente.
    - Endpoint público para o cadastro inicial de gestores.
    """
    return await gestor_controller.create_new_account(gestor_in=gestor_in)