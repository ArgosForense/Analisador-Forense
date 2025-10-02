from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.config import settings
from app.models.gestor_model import Gestor
from app.models.user_model import Usuario
from app.models.empresa_model import Empresa
from app.schemas.gestor_schema import GestorCreateSchema
from app.schemas.empresa_schema import EmpresaCreateSchema
from app.schemas.auth_schema import LoginSchema

# Importando os repositórios para desacoplar o acesso ao banco
from app.repositories.gestor_repository import gestor_repository
from app.repositories.empresa_repository import empresa_repository
from app.repositories.user_repository import user_repository

class AuthService:

    def _autenticar_gestor(self, db: Session, email: str, senha: str) -> Gestor | None:
        """Busca e autentica um gestor."""
        gestor = gestor_repository.get_by_email(db, email=email)
        if not gestor or not verify_password(senha, gestor.senha):
            return None
        return gestor

    def _autenticar_usuario(self, db: Session, email: str, senha: str) -> Usuario | None:
        """Busca e autentica um usuário."""
        usuario = user_repository.get_by_email(db, email=email)
        if not usuario or not verify_password(senha, usuario.senha):
            return None
        return usuario

    ###def login_for_access_token(self, db: Session, form_data: OAuth2PasswordRequestForm):
    def login_for_access_token(self, db: Session, *, login_data: LoginSchema):
        """
        Lida com o processo de login para Gestor ou Usuário, gerando access e refresh tokens.
        """
        ###gestor = self._autenticar_gestor(db, email=form_data.username, senha=form_data.password)
        gestor = self._autenticar_gestor(db, email=login_data.email, senha=login_data.senha)
        if gestor:
            data = {"sub": str(gestor.id), "tipo": "gestor"}
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_token_expires = timedelta(days=7)
            
            ### access_token = create_access_token(str(gestor.id), "gestor", expires_delta=access_token_expires)
            ### refresh_token = create_access_token(str(gestor.id), "gestor", expires_delta=refresh_token_expires)
            access_token = create_access_token(data=data, expires_delta=access_token_expires)
            refresh_token = create_access_token(data=data, expires_delta=refresh_token_expires)
            
            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "tipo": "gestor"}

        ###usuario = self._autenticar_usuario(db, email=form_data.username, senha=form_data.password)
        usuario = self._autenticar_usuario(db, email=login_data.email, senha=login_data.senha)
        if usuario:
            if not usuario.is_ativo():
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário desativado.")
            
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_token_expires = timedelta(days=7)
            
            data = {"sub": str(usuario.id), "tipo": "usuario"}
            ### access_token = create_access_token(str(usuario.id), "usuario", expires_delta=access_token_expires)
            ### refresh_token = create_access_token(str(usuario.id), "usuario", expires_delta=refresh_token_expires)
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_token_expires = timedelta(days=7)
            
            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "tipo": "usuario"}

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail ou senha incorretos.")

    def refresh_token(self, current_user: Gestor | Usuario):
        """
        Gera um novo access_token a partir de um token de atualização válido.
        """
        user_id = current_user.id
        user_type = "gestor" if isinstance(current_user, Gestor) else "usuario"
        
        #access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        #new_access_token = create_access_token(data={"sub": str(user_id), "tipo": user_type})
        data = {"sub": str(user_id), "tipo": user_type}
        new_access_token = create_access_token(data=data)
        
        return {"access_token": new_access_token, "token_type": "bearer", "tipo": user_type}

    def create_gestor_account(self, db: Session, gestor_in: GestorCreateSchema):
        """Cria uma nova conta de gestor."""
        gestor_existente = gestor_repository.get_by_email(db, email=gestor_in.email)
        if gestor_existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Já existe um gestor com este e-mail.")
            
        hashed_password = get_password_hash(gestor_in.senha)
        return gestor_repository.create(db, gestor_in=gestor_in, hashed_password=hashed_password)

    def register_empresa(self, db: Session, empresa_in: EmpresaCreateSchema):
        """Registra uma nova empresa."""
        empresa_existente = empresa_repository.get_by_cnpj(db, cnpj=empresa_in.cnpj)
        if empresa_existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Já existe uma empresa com este CNPJ.")
            
        return empresa_repository.create(db, empresa_in=empresa_in)

auth_service = AuthService()