from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import init_db
from fastapi.middleware.cors import CORSMiddleware  
from app.api.routes import auth_router, user_router, perfil_router, permissao_router, empresa_router, gestor_router


# Garante que o banco conecte antes do servidor começar a receber requisições.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- INICIO
    # Inicia conexão com MongoDB ao ligar o servidor
    print("🚀 Iniciando conexão com MongoDB...")
    await init_db()
    print("MongoDB Conectado e Models Inicializados!")
    
    yield
    # --- FIM (Shutdown) ---
    # Código para rodar ao desligar (opcional)
    print("🛑 Desligando aplicação...")
    

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="Analisador Forense API",
    description="Sistema para gestão de usuários, perfis e permissões.",
    version="2.0.0",
    lifespan=lifespan
)

# --- CONFIGURAÇÃO DO CORS (NOVO) ---
origins = [
    "http://localhost:5173", # URL do Vite (Front-end)
    "http://localhost:3000",
    "http://127.0.0.1:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------------


# ROTAS
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
    return {"status": "API is running", "database": "MongoDB"}

# para rodar o código, executar no terminal: uvicorn main:app --reload