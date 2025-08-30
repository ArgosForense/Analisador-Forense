from fastapi import APIRouter, Depends, HTTPException
from models import Gestor
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import GestorSchema
from sqlalchemy.orm import Session


auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])

@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do sistema.
    """
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(gestor_schema: GestorSchema, session: Session = Depends(pegar_sessao)):
    gestor = session.query(Gestor).filter((Gestor.email == gestor_schema.email) & (Gestor.empresa_id == gestor_schema.empresa_id)).first()
    if gestor:
        
        return HTTPException(status_code=400, detail="Já existe um gestor com esse email nessa empresa.")
    else:
        senha_criptografada = bcrypt_context.hash(gestor_schema.senha)
        novo_gestor = Gestor(gestor_schema.nome, gestor_schema.email, senha_criptografada, gestor_schema.empresa_id)
        session.add(novo_gestor)
        session.commit()
        return {"mensagem": f"Gestor cadastrado com sucesso: {gestor_schema.email}"}