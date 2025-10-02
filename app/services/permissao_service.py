from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.permissao_repository import permissao_repository
from app.schemas.permissao_schema import PermissaoCreateSchema

class PermissaoService:
    def create_permissao(self, db: Session, *, permissao_in: PermissaoCreateSchema):
        permissao_existente = permissao_repository.get_by_name(db, name=permissao_in.nome)
        if permissao_existente:
            raise HTTPException(status_code=400, detail="Permissão já existe")
        
        return permissao_repository.create(db, nome=permissao_in.nome)

permissao_service = PermissaoService()