from sqlalchemy.orm import Session
from typing import List
from app.services.permissao_service import permissao_service
from app.schemas.permissao_schema import PermissaoCreateSchema, PermissaoUpdateSchema

class PermissaoController:
    def listar_permissoes(self, db: Session):
        return permissao_service.listar_permissoes(db)

    def create_new_permissao(self, db: Session, *, permissao_in: PermissaoCreateSchema):
        return permissao_service.criar_permissao(db, permissao_in=permissao_in)

    def update_permissao(self, db: Session, permissao_id: int, permissao_in: PermissaoUpdateSchema):
        return permissao_service.atualizar_permissao(db, permissao_id, permissao_in)

    def delete_permissao(self, db: Session, permissao_id: int):
        return permissao_service.deletar_permissao(db, permissao_id)

permissao_controller = PermissaoController()