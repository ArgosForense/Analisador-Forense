from datetime import timedelta
from typing import Any
from fastapi import HTTPException, status
from app.core.security import verificar_senha, create_access_token, gerar_hash_senha
from app.core.config import settings
from app.models.user_model import Usuario
from app.models.gestor_model import Gestor
from app.repositories.user_repository import user_repository
from app.repositories.gestor_repository import gestor_repository
from app.repositories.empresa_repository import empresa_repository
from app.schemas.auth_schema import LoginSchema
from app.schemas.gestor_schema import GestorCreateSchema
from app.schemas.empresa_schema import EmpresaCreateSchema

class AuthService:

    async def _autenticar_gestor(self, email: str, senha: str) -> Gestor | None:
        print(f"🔍 [DEBUG] Tentando autenticar Gestor: {email}")
        gestor = await gestor_repository.get_by_email(email=email)
        
        if not gestor:
            print(f"❌ [DEBUG] Gestor não encontrado no banco.")
            return None
            
        senha_valida = verificar_senha(senha, gestor.senha)
        print(f"🔑 [DEBUG] Gestor encontrado (ID: {gestor.id}). Senha válida? {senha_valida}")
        
        if not senha_valida:
            return None
        return gestor

    async def _autenticar_usuario(self, email: str, senha: str) -> Usuario | None:
        print(f"🔍 [DEBUG] Tentando autenticar Usuário: {email}")
        usuario = await user_repository.get_by_email(email=email)
        
        if not usuario:
            return None
            
        if not verificar_senha(senha, usuario.senha):
            print(f"❌ [DEBUG] Senha incorreta para usuário {email}")
            return None
        return usuario

    async def login_for_access_token(self, *, login_data: LoginSchema):
        gestor = await self._autenticar_gestor(email=login_data.email, senha=login_data.senha)
        
        if gestor:
            print("✅ [DEBUG] Login de Gestor OK!")
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_token_expires = timedelta(days=7)
            
            # CORREÇÃO AQUI: Usando 'subject' e 'additional_claims'
            access_token = create_access_token(
                subject=gestor.id, 
                expires_delta=access_token_expires,
                additional_claims={"tipo": "gestor"}
            )
            refresh_token = create_access_token(
                subject=gestor.id, 
                expires_delta=refresh_token_expires,
                additional_claims={"tipo": "gestor"}
            )
            
            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "tipo": "gestor"}

        usuario = await self._autenticar_usuario(email=login_data.email, senha=login_data.senha)
        
        if usuario:
            if not usuario.is_ativo():
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário desativado.")
           
            print("✅ [DEBUG] Login de Usuário OK!")
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_token_expires = timedelta(days=7)
            
            # CORREÇÃO AQUI TAMBÉM
            access_token = create_access_token(
                subject=usuario.id, 
                expires_delta=access_token_expires,
                additional_claims={"tipo": "usuario"}
            )
            refresh_token = create_access_token(
                subject=usuario.id, 
                expires_delta=refresh_token_expires,
                additional_claims={"tipo": "usuario"}
            )
            
            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "tipo": "usuario"}

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail ou senha incorretos.")

    def refresh_token(self, usuario_logado: Gestor | Usuario):
        user_id = usuario_logado.id
        user_type = "gestor" if isinstance(usuario_logado, Gestor) else "usuario"
        
        # CORREÇÃO AQUI TAMBÉM
        new_access_token = create_access_token(
            subject=user_id,
            additional_claims={"tipo": user_type}
        )
        
        return {"access_token": new_access_token, "token_type": "bearer", "tipo": user_type}

    async def criar_conta_gestor(self, gestor_in: GestorCreateSchema):
        gestor_existente = await gestor_repository.get_by_email(email=gestor_in.email)
        if gestor_existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Já existe um gestor com este e-mail.")
            
        hashed_password = gerar_hash_senha(gestor_in.senha)
        print(f"🛠️ [DEBUG] Criando gestor {gestor_in.email}. Hash gerado: {hashed_password[:10]}...")
        
        novo_gestor = Gestor(
            nome=gestor_in.nome,
            email=gestor_in.email,
            senha=hashed_password,
            empresa=gestor_in.empresa_id
        )
        await novo_gestor.create()
        return novo_gestor

    async def register_empresa(self, empresa_in: EmpresaCreateSchema):
        empresa_existente = await empresa_repository.get_by_cnpj(cnpj=empresa_in.cnpj)
        if empresa_existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Já existe uma empresa com este CNPJ.")
        return await empresa_repository.create(obj_in=empresa_in)

auth_service = AuthService()