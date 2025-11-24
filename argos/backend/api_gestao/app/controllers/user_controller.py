from app.schemas.user_schema import UserCreateSchema
from app.services.user_service import user_service
from app.models.gestor_model import Gestor
from beanie import PydanticObjectId

class UserController:
    
    async def listar_usuarios(self):
        return await user_service.listar_todos()
    
    async def criar_novo_usuario(self, user_in: UserCreateSchema, current_gestor: Gestor):
        return await user_service.criar_usuario(user_in=user_in, gestor=current_gestor)
    
    async def ativar_usuario(self, user_id: PydanticObjectId):
        return await user_service.ativar_usuario(user_id=user_id)

    async def desativar_usuario(self, user_id: PydanticObjectId):
        return await user_service.desativar_usuario(user_id=user_id)
    
    async def deletar_usuario(self, user_id: PydanticObjectId):
        return await user_service.deletar_usuario(user_id=user_id)

user_controller = UserController()