from app.services.permissao_service import permissao_service
from app.schemas.permissao_schema import PermissaoCreateSchema, PermissaoUpdateSchema
from beanie import PydanticObjectId

class PermissaoController:
    async def listar_permissoes(self):
        return await permissao_service.listar_permissoes()

    async def create_new_permissao(self, permissao_in: PermissaoCreateSchema):
        return await permissao_service.criar_permissao(permissao_in=permissao_in)

    async def update_permissao(self, permissao_id: PydanticObjectId, permissao_in: PermissaoUpdateSchema):
        return await permissao_service.atualizar_permissao(permissao_id, permissao_in)

    async def delete_permissao(self, permissao_id: PydanticObjectId):
        return await permissao_service.deletar_permissao(permissao_id)

permissao_controller = PermissaoController()