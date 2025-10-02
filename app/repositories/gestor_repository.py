from sqlalchemy.orm import Session
from app.models.gestor_model import Gestor
from app.schemas.gestor_schema import GestorCreateSchema

from .base_repository import BaseRepository

class GestorRepository(BaseRepository[Gestor]):
    def get_by_email(self, db: Session, *, email: str) -> Gestor | None:
        return db.query(Gestor).filter(Gestor.email == email).first()

    def create(self, db: Session, *, gestor_in: GestorCreateSchema, hashed_password: str) -> Gestor:
        db_gestor = Gestor(
            nome=gestor_in.nome,
            email=gestor_in.email,
            senha=hashed_password,
            empresa_id=gestor_in.empresa_id
        )
        db.add(db_gestor)
        db.commit()
        db.refresh(db_gestor)
        return db_gestor

gestor_repository = GestorRepository(Gestor)