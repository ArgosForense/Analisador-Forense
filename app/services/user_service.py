from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.user_schema import UserCreateSchema
from app.repositories.user_repository import user_repository
from app.core.security import (
    generate_random_password, 
    get_password_hash, 
    generate_institutional_email, 
    send_credentials_email
)
from app.models.gestor_model import Gestor

class UserService:
    def create_user(self, db: Session, *, user_in: UserCreateSchema, gestor: Gestor):
        random_password = generate_random_password()
        hashed_password = get_password_hash(random_password)
        institutional_email = generate_institutional_email(user_in.nome)

        if user_repository.get_by_email(db, email=institutional_email):
            raise HTTPException(status_code=400, detail="Um usuário com este nome já existe, gerando um e-mail duplicado.")

        new_user = user_repository.create_with_gestor(
            db, obj_in=user_in, gestor_id=gestor.id, hashed_password=hashed_password, institutional_email=institutional_email
        )

        send_credentials_email(
            personal_email=user_in.email,
            institutional_email=institutional_email,
            password=random_password,
        )
        return new_user

    def activate_user(self, db: Session, *, user_id: int):
        user = user_repository.get(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        user.ativar()
        return user_repository.save(db, user=user)

    def deactivate_user(self, db: Session, *, user_id: int):
        user = user_repository.get(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        user.desativar()
        return user_repository.save(db, user=user)

user_service = UserService()