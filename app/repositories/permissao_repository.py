# from sqlalchemy.orm import Session
# from typing import List
# from ..models import models

# class PermissaoRepository:
#     def get_by_ids(self, db: Session, ids: List[int]) -> List[models.Permissao]:
#         return db.query(models.Permissao).filter(models.Permissao.id.in_(ids)).all()

# permissao_repository = PermissaoRepository()

from sqlalchemy.orm import Session
from app.models.permissao_model import Permissao

from .base_repository import BaseRepository

class PermissaoRepository(BaseRepository[Permissao]):
    def get_by_name(self, db: Session, *, name: str) -> Permissao | None:
        return db.query(Permissao).filter(Permissao.nome == name).first()
    
    def create(self, db: Session, *, nome: str) -> Permissao:
        db_obj = Permissao(nome=nome)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_ids(self, db: Session, *, ids: list[int]) -> list[Permissao]:
        return db.query(self.model).filter(self.model.id.in_(ids)).all()

permissao_repository = PermissaoRepository(Permissao)