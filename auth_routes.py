from fastapi import APIRouter, Depends, HTTPException
from models import Gestor, Empresa
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import GestorSchema, EmpresaSchema
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
    """Resumo: Essa é a rota para criação de conta para gestores vinculados a uma empresa já existente no sistema.
    
    OBS.: Foi criada a restrição de apenas gestores, pois as contas de usuários serão criados pelos gestores.
    """
    gestor = session.query(Gestor).filter((Gestor.email == gestor_schema.email) & (Gestor.empresa_id == gestor_schema.empresa_id)).first()
    if gestor:
        
        return HTTPException(status_code=400, detail="Já existe um gestor com esse email nessa empresa.")
    else:
        senha_criptografada = bcrypt_context.hash(gestor_schema.senha)
        novo_gestor = Gestor(gestor_schema.nome, gestor_schema.email, senha_criptografada, gestor_schema.empresa_id)
        session.add(novo_gestor)
        session.commit()
        return {"mensagem": f"Gestor cadastrado com sucesso. Gestor: {gestor_schema.email}"}
    
@auth_router.post("/cadastrar_empresa")
async def cadastrar_empresa(empresa_schema: EmpresaSchema, session: Session = Depends(pegar_sessao)):
    """Resumo: Rota para cadastro de uma nova empresa no sistema. Apenas empresas novas podem ser cadastradas.
    """
    empresa = session.query(Empresa).filter(Empresa.cnpj == empresa_schema.cnpj).first()
    if empresa:
        return HTTPException(status_code=400, detail="Já existe uma empresa com esse CNPJ.")
    else:
        nova_empresa = Empresa(empresa_schema.nome, empresa_schema.cnpj) 
        session.add(nova_empresa)
        session.commit()
        return {"mensagem": f"Empresa cadastrada com sucesso. Empresa: {empresa_schema.nome}"}