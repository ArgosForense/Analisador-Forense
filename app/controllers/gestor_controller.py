from sqlalchemy.orm import Session
from app.services.gestor_service import gestor_service
from app.schemas.gestor_schema import GestorCreateSchema

class GestorController:
    def create_new_account(self, db: Session, *, gestor_in: GestorCreateSchema):
        return gestor_service.create_gestor_account(db=db, gestor_in=gestor_in)

gestor_controller = GestorController()