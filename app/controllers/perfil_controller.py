from sqlalchemy.orm import Session
from app.services.perfil_service import perfil_service
from app.schemas.perfil_schema import PerfilCreateSchema

class PerfilController:
    def create_new_perfil(self, db: Session, *, perfil_in: PerfilCreateSchema):
        return perfil_service.criar_perfil(db, perfil_in=perfil_in)

perfil_controller = PerfilController()