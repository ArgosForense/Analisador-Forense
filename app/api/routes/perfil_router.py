from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import dependencies
from app.schemas.perfil_schema import PerfilCreateSchema, PerfilResponseSchema
from app.controllers.perfil_controller import perfil_controller

router = APIRouter(
    prefix="/perfis", 
    tags=["Perfis"], 
    dependencies=[Depends(dependencies.nivel_acesso_gestor)]
)

@router.post("/", response_model=PerfilResponseSchema, status_code=201)
def create_perfil(
    *,
    perfil_in: PerfilCreateSchema,
    db: Session = Depends(dependencies.get_db)
):
    """
    Cria um novo perfil com um conjunto de permissões.
    - **Acesso:** Apenas Gestores.
    """
    return perfil_controller.create_new_perfil(db=db, perfil_in=perfil_in)