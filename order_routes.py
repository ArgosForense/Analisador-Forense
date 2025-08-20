from fastapi import APIRouter

order_router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@order_router.get("/")
async def usuarios():
    return {"mensagem": "Você acessou a rota de usuários"}