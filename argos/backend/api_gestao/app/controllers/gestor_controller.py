from app.services.auth_service import auth_service
from app.schemas.gestor_schema import GestorCreateSchema

class GestorController:
    async def create_new_account(self, gestor_in: GestorCreateSchema):
        # Nota: Usamos o auth_service aqui pois ele centraliza a criação segura
        return await auth_service.criar_conta_gestor(gestor_in=gestor_in)

gestor_controller = GestorController()