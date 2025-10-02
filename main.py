from fastapi import FastAPI
from app.core.database import create_db_and_tables
from app.api.routes import auth_router, user_router, perfil_router, permissao_router, empresa_router, gestor_router


# Função que será executada na inicialização da aplicação
def startup_event():
    """
    Cria as tabelas no banco de dados, caso elas não existam.
    """
    create_db_and_tables()

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="Analisador Forense API",
    description="Sistema para gestão de usuários, perfis e permissões.",
    version="1.0.0"
)

# Registra a função de startup
app.add_event_handler("startup", startup_event)

# Inclui todos os roteadores na aplicação
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(perfil_router.router)
app.include_router(permissao_router.router)
app.include_router(empresa_router.router)
app.include_router(gestor_router.router)

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raiz para verificar se a API está funcionando.
    """
    return {"status": "API is running"}

# para rodar o código, executar no terminal: uvicorn main:app --reload