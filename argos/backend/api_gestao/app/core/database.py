from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings

# Importamos os modelos para registrá-los no Beanie
from app.models.user_model import Usuario
from app.models.gestor_model import Gestor
from app.models.empresa_model import Empresa
from app.models.perfil_model import Perfil
from app.models.permissao_model import Permissao

async def init_db():
    """
    Inicializa a conexão com o MongoDB e configura o Beanie (ODM).
    """
    # Cria o cliente do Motor (Driver Async)
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    # Seleciona o banco de dados
    database = client.argos_db
    
    # Inicializa o Beanie com os modelos de documentos
    await init_beanie(
        database=database,
        document_models=[
            Usuario,
            Gestor,
            Empresa,
            Perfil,
            Permissao
        ]
    )