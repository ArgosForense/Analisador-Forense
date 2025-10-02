from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import dependencies
from app.schemas.gestor_schema import GestorCreateSchema, GestorResponseSchema
from app.controllers.gestor_controller import gestor_controller

router = APIRouter(prefix="/gestores", tags=["Gestores"])

@router.post("/criar_conta", response_model=GestorResponseSchema, status_code=201)
def create_account(
    *,
    gestor_in: GestorCreateSchema,
    db: Session = Depends(dependencies.get_db)
):
    """
    Cria uma nova conta de gestor, vinculada a uma empresa existente.
    - Endpoint público para o cadastro inicial de gestores.
    """
    return gestor_controller.create_new_account(db=db, gestor_in=gestor_in)