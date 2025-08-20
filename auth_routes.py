from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])

@auth_router.get("/")
async def autenticar():
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False}