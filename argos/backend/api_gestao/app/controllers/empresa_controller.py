from app.services.auth_service import auth_service
from app.schemas.empresa_schema import EmpresaCreateSchema

class EmpresaController:
    async def create_new_empresa(self, empresa_in: EmpresaCreateSchema):
        return await auth_service.register_empresa(empresa_in=empresa_in)

empresa_controller = EmpresaController()