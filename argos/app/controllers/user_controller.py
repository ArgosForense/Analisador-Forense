from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreateSchema
from app.services.user_service import user_service
from app.models.gestor_model import Gestor

class UserController:
    
    def listar_usuarios(self, db: Session):
        return user_service.listar_todos(db)
    
    def criar_novo_usuario(self, db: Session, *, user_in: UserCreateSchema, current_gestor: Gestor):
        # A lógica de negócio está toda no serviço
        return user_service.criar_usuario(db, user_in=user_in, gestor=current_gestor)
    
    def ativar_usuario(self, db: Session, *, user_id: int):
        return user_service.ativar_usuario(db, user_id=user_id)

    def desativar_usuario(self, db: Session, *, user_id: int):
        return user_service.desativar_usuario(db, user_id=user_id)
    
    def deletar_usuario(self, db: Session, *, user_id: int):
        return user_service.deletar_usuario(db, user_id=user_id)

user_controller = UserController()