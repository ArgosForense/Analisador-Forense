from typing import Optional
from beanie import PydanticObjectId
from .base_repository import BaseRepository
from app.models.user_model import Usuario
from app.schemas.user_schema import UserCreateSchema, UserUpdateSchema

class UserRepository(BaseRepository[Usuario, UserCreateSchema, UserUpdateSchema]):
    
    async def get_by_email(self, email: str) -> Optional[Usuario]:
        # find_one retorna o primeiro match
        return await self.model.find_one(Usuario.email == email)

    async def get_all_with_profile(self):
        # fetch_links=True faz o "JOIN" automático trazendo os dados do Perfil linkado
        return await self.model.find_all().find(fetch_links=True).to_list()

user_repository = UserRepository(Usuario)