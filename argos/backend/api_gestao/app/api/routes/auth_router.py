from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api import dependencies
from app.services.auth_service import auth_service
from app.schemas.token_schema import Token, TokenResponseSchema
from app.schemas.gestor_schema import GestorCreateSchema, GestorResponseSchema
from app.schemas.empresa_schema import EmpresaCreateSchema, EmpresaResponseSchema
from app.models.user_model import Usuario
from app.models.gestor_model import Gestor
from app.schemas.auth_schema import LoginSchema

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=TokenResponseSchema)
async def login(login_data: LoginSchema):
    """
    Autentica um gestor ou usuário e retorna tokens de acesso e de atualização.
    O 'username' do formulário é o e-mail.
    """
    return await auth_service.login_for_access_token(login_data=login_data)

@router.post("/login-form", response_model=TokenResponseSchema, include_in_schema=False)
async def login_form(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Rota para testes de autorização via documentação (Swagger UI).
    Converte o formulário padrão do Swagger para o Schema de Login do sistema.
    """
    # Adaptador: O Swagger envia 'username', nosso sistema espera 'email'
    login_data = LoginSchema(email=form_data.username, senha=form_data.password)
    return await auth_service.login_for_access_token(login_data=login_data)

@router.get("/refresh_token", response_model=Token)
def refresh_access_token(usuario_logado: Gestor | Usuario = Depends(dependencies.verificar_token)):
    """
    Gera um novo token de acesso (access_token) a partir de um token válido.
    
    Isso permite que o cliente renove seu token de acesso sem precisar
    enviar o login e a senha novamente.
    """
    return auth_service.refresh_token(usuario_logado=usuario_logado)

# --- Rotas Públicas (que estavam faltando) ---

@router.post("/criar_conta", response_model=GestorResponseSchema, status_code=201)
async def create_account(gestor_in: GestorCreateSchema):
    """
    Cria uma nova conta de gestor.
    - Endpoint público para o cadastro inicial.
    """
    return await auth_service.criar_conta_gestor(gestor_in=gestor_in)

@router.post("/cadastrar_empresa", response_model=EmpresaResponseSchema, status_code=201)
async def register_empresa(empresa_in: EmpresaCreateSchema):
    """
    Cadastra uma nova empresa no sistema.
    """
    return await auth_service.register_empresa(empresa_in=empresa_in)