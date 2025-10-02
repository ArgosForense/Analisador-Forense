from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from app.models.user_model import Usuario
from app.schemas.user_schema import UserCreateSchema

class UserRepository(BaseRepository[Usuario]):
    def get(self, db: Session, *, user_id: int) -> Usuario | None:
        return db.query(Usuario).filter(Usuario.id == user_id).first()
    
    def get_email(self, db: Session, *, email: str) -> Usuario | None:
        return db.query(Usuario).filter(Usuario.email == email).first()

    def create_with_gestor(
        self, db: Session, *, obj_in: UserCreateSchema, gestor_id: int, hashed_password: str, institutional_email: str
    ) -> Usuario:
        db_obj = Usuario(
            nome=obj_in.nome,
            email=institutional_email,
            senha=hashed_password,
            perfil_id=obj_in.perfil_id,
            gestor_id=gestor_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def save(self, db: Session, *, user: Usuario) -> Usuario:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

user_repository = UserRepository(Usuario)