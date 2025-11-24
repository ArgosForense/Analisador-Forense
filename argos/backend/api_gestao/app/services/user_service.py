from fastapi import HTTPException, status
from typing import List
from beanie import PydanticObjectId
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
    
    async def listar_todos(self) -> List[Usuario]:
        # Aqui já usamos fetch_links no repositório, então funciona
        return await user_repository.get_all_with_profile()
    
    async def criar_usuario(self, user_in: UserCreateSchema, gestor: Gestor):
        random_password = gerar_senha_aleatoria()
        hashed_password = gerar_hash_senha(random_password)
        institutional_email = gerar_email_institucional(user_in.nome)

        if await user_repository.get_by_email(email=institutional_email):
            raise HTTPException(status_code=400, detail="Já existe um usuário com este nome/email.")

        new_user = Usuario(
            nome=user_in.nome,
            email=institutional_email,
            senha=hashed_password,
            perfil=user_in.perfil_id,
            gestor=gestor.id,
            status="ATIVO"
        )
        
        await new_user.create()
        
        # --- IMPORTANTE: Carrega o perfil para retornar no JSON de resposta ---
        await new_user.fetch_all_links()

        enviar_email_credenciais(
            personal_email=user_in.email,
            institutional_email=institutional_email,
            password=random_password,
        )
        return new_user

    async def ativar_usuario(self, user_id: PydanticObjectId):
        user = await user_repository.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        
        user.ativar()
        await user.save()
        
        # --- CORREÇÃO AQUI ---
        # Força o Beanie a buscar os dados reais do Perfil (nome, id)
        # para satisfazer o UserResponseSchema
        await user.fetch_all_links()
        
        return user

    async def desativar_usuario(self, user_id: PydanticObjectId):
        user = await user_repository.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        
        user.desativar()
        await user.save()
        
        # --- CORREÇÃO AQUI ---
        await user.fetch_all_links()
        
        return user

    async def deletar_usuario(self, user_id: PydanticObjectId):
        user = await user_repository.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        await user.delete()
        return True
    
user_service = UserService()