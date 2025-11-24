from app.services.perfil_service import perfil_service
from app.schemas.perfil_schema import PerfilCreateSchema
from beanie import PydanticObjectId

class PerfilController:
    async def create_new_perfil(self, perfil_in: PerfilCreateSchema):
        return await perfil_service.criar_perfil(perfil_in=perfil_in)

    async def listar_todos_perfis(self):
        return await perfil_service.listar_perfis()
    
    async def delete_perfil(self, perfil_id: PydanticObjectId):
        return await perfil_service.deletar_perfil(perfil_id=perfil_id)

perfil_controller = PerfilController()