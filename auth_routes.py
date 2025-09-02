from fastapi import APIRouter, Depends, HTTPException
from models import Gestor, Empresa, Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import GestorSchema, EmpresaSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])


def criar_token(id, tipo,duracao_token=timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(tz=timezone.utc) + duracao_token
    dicionario_informacoes = {
        "sub": str(id),
        "exp": data_expiracao,
        "tipo": tipo  # Gestor ou Usuario
    }
    jwt_codificado = jwt.encode(dicionario_informacoes, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado



    
# Pega as informações do token
@auth_router.get("/refresh_token")
async def use_refresh_token(obj_autenticado = Depends(verificar_token)):
    """Resumo: Rota para renovar o token de acesso (access_token) usando o token de atualização (refresh_token).
    """
    if isinstance(obj_autenticado, Gestor):
        access_token = criar_token(obj_autenticado.id, "gestor")
        tipo = "gestor"
    elif isinstance(obj_autenticado, Usuario):
        access_token = criar_token(obj_autenticado.id, "usuario")
        tipo = "usuario"
    else:
        raise HTTPException(status_code=401, detail="Token inválido ou usuário não autenticado.")
    #access_token = criar_token(gestor.id)
    #access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "tipo": tipo
    }
    

def autenticar_gestor(email, senha, session):
    gestor = session.query(Gestor).filter(Gestor.email == email).first()
    if not gestor:
        return False
    elif not bcrypt_context.verify(senha, gestor.senha):
        return False
    return gestor

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

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
        
        raise HTTPException(status_code=400, detail="Já existe um gestor com esse email nessa empresa.")
    else:
        senha_criptografada = bcrypt_context.hash(gestor_schema.senha)
        novo_gestor = Gestor(gestor_schema.nome, gestor_schema.email, senha_criptografada, gestor_schema.empresa_id)
        session.add(novo_gestor)
        session.commit()
        return {"mensagem": f"Gestor cadastrado com sucesso. Gestor: {gestor_schema.email}"}

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    """Resumo: Rota para login de Gestores ou Usuários no sistema. 
    """
    gestor = autenticar_gestor(login_schema.email, login_schema.senha, session)
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    
    if not usuario and not gestor:
        raise HTTPException(status_code=400, detail="Conta não encontrada ou credenciais incorretas.")
    elif gestor:
        access_token = criar_token(gestor.id, "gestor")
        refresh_token = criar_token(gestor.id, "gestor", duracao_token=timedelta(days=7)) # Token de atualização com duração maior (7 dias)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "tipo": "gestor"
        }
    else:
        access_token = criar_token(usuario.id,"usuario")
        refresh_token = criar_token(usuario.id, "usuario", duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "tipo": "usuario"
        }
        
@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    """Resumo: Rota exclusiva para testes de autorização via OAuth2 na documentação automática do FastAPI. 
    - Ao invés de fazer requisições manuais, pode-se usar a documentação automática do FastAPI. 
    - Uso do formulário da documentação automática do FastAPI para passar os dados (username e password)
    """
    gestor = autenticar_gestor(dados_formulario.username, dados_formulario.password, session)
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    
    if not usuario and not gestor:
        raise HTTPException(status_code=400, detail="Conta não encontrada ou credenciais incorretas.")
    elif gestor:
        access_token = criar_token(gestor.id, "gestor")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "tipo": "gestor"
        }
    else:
        access_token = criar_token(usuario.id,"usuario")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "tipo": "usuario"
        }                

@auth_router.post("/cadastrar_empresa")
async def cadastrar_empresa(empresa_schema: EmpresaSchema, session: Session = Depends(pegar_sessao)):
    """Resumo: Rota para cadastro de uma nova empresa no sistema. Apenas empresas novas podem ser cadastradas.
    """
    empresa = session.query(Empresa).filter(Empresa.cnpj == empresa_schema.cnpj).first()
    if empresa:
        raise HTTPException(status_code=400, detail="Já existe uma empresa com esse CNPJ.")
    else:
        nova_empresa = Empresa(empresa_schema.nome, empresa_schema.cnpj) 
        session.add(nova_empresa)
        session.commit()
        return {"mensagem": f"Empresa cadastrada com sucesso. Empresa: {empresa_schema.nome}"}