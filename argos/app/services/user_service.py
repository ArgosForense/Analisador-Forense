from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from app.schemas.user_schema import UserCreateSchema
from app.repositories.user_repository import user_repository
from app.core.security import (
    gerar_senha_aleatoria, 
    gerar_hash_senha, 
    gerar_email_institucional, 
    enviar_email_credenciais
)
from app.models.gestor_model import Gestor
from app.models.user_model import Usuario

class UserService:
    
    def listar_todos(self, db: Session) -> List[Usuario]:
        return user_repository.get_all_users(db)
    
    def criar_usuario(self, db: Session, *, user_in: UserCreateSchema, gestor: Gestor):
        random_password = gerar_senha_aleatoria()
        hashed_password = gerar_hash_senha(random_password)
        institutional_email = gerar_email_institucional(user_in.nome)

        if user_repository.get_email(db, email=institutional_email):
            raise HTTPException(status_code=400, detail="Já existe um usuário com este nome.")

        new_user = user_repository.create_with_gestor(
            db, obj_in=user_in, gestor_id=gestor.id, hashed_password=hashed_password, institutional_email=institutional_email
        )

        enviar_email_credenciais(
            personal_email=user_in.email,
            institutional_email=institutional_email,
            password=random_password,
        )
        return new_user

    def ativar_usuario(self, db: Session, *, user_id: int):
        user = user_repository.get(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        user.ativar()
        return user_repository.save(db, user=user)

    def desativar_usuario(self, db: Session, *, user_id: int):
        user = user_repository.get(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        user.desativar()
        return user_repository.save(db, user=user)

    def deletar_usuario(self, db: Session, *, user_id: int):
        user = user_repository.get(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        return user_repository.remove(db, id=user_id)
    
user_service = UserService()