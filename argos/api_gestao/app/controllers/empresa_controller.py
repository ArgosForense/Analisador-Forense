from sqlalchemy.orm import Session
from app.services.empresa_service import empresa_service
from app.schemas.empresa_schema import EmpresaCreateSchema

class EmpresaController:
    def create_new_empresa(self, db: Session, *, empresa_in: EmpresaCreateSchema):
        return empresa_service.register_empresa(db=db, empresa_in=empresa_in)

empresa_controller = EmpresaController()