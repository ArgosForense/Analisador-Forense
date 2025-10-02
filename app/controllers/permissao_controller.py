from sqlalchemy.orm import Session
from app.services.permissao_service import permissao_service
from app.schemas.permissao_schema import PermissaoCreateSchema

class PermissaoController:
    def create_new_permissao(self, db: Session, *, permissao_in: PermissaoCreateSchema):
        return permissao_service.criar_permissao(db, permissao_in=permissao_in)

permissao_controller = PermissaoController()