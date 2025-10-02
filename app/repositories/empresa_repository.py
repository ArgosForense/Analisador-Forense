from sqlalchemy.orm import Session
from app.models.empresa_model import Empresa
from app.schemas.empresa_schema import EmpresaCreateSchema

from .base_repository import BaseRepository

class EmpresaRepository(BaseRepository[Empresa]):
    def get_by_cnpj(self, db: Session, *, cnpj: str) -> Empresa | None:
        return db.query(Empresa).filter(Empresa.cnpj == cnpj).first()
    
    def create(self, db: Session, *, empresa_in: EmpresaCreateSchema) -> Empresa:
        db_empresa = Empresa(nome=empresa_in.nome, cnpj=empresa_in.cnpj)
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
        return db_empresa

empresa_repository = EmpresaRepository(Empresa)