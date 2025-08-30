from fastapi import APIRouter, Depends
from models import Gestor
from dependencies import pegar_sessao
from main import bcrypt_context



auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])

@auth_router.get("/")
async def home():
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(email: str, senha: str, nome: str, empresa_id: int, session = Depends(pegar_sessao)):
    gestor = session.query(Gestor).filter((Gestor.email == email) & (Gestor.empresa_id == empresa_id)).first()
    if gestor:
        #já existe um gestor com esse email nessa mesma empresa
        return {"mensagem": "Já existe um gestor com esse email!"}
    else:
        senha_criptografada = bcrypt_context.hash(senha)
        novo_gestor = Gestor(nome, email, senha_criptografada, empresa_id)
        session.add(novo_gestor)
        session.commit()
        return {"mensagem": "Conta do Gestor criada com sucesso!"} ## retorna cod: 200