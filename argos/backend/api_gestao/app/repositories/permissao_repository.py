from sqlalchemy.orm import Session
from typing import List
from app.models.permissao_model import Permissao
from .base_repository import BaseRepository

class PermissaoRepository(BaseRepository[Permissao]):
    def get_by_name(self, db: Session, *, name: str) -> Permissao | None:
        return db.query(Permissao).filter(Permissao.nome == name).first()
    
    # método para a listagem
    def get_all(self, db: Session) -> List[Permissao]:
        return db.query(Permissao).all()
    
    def get_by_ids(self, db: Session, *, ids: list[int]) -> list[Permissao]:
        return db.query(self.model).filter(self.model.id.in_(ids)).all()

permissao_repository = PermissaoRepository(Permissao)