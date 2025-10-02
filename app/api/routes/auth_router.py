from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
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
def login(*,
    db: Session = Depends(dependencies.get_db), 
    ###form_data: OAuth2PasswordRequestForm = Depends()
    login_data: LoginSchema
):
    """
    Autentica um gestor ou usuário e retorna tokens de acesso e de atualização.
    O 'username' do formulário é o e-mail.
    """
    ###return auth_service.login_for_access_token(db=db, form_data=form_data)
    return auth_service.login_for_access_token(db=db, login_data=login_data)

@router.post("/login-form", response_model=TokenResponseSchema, include_in_schema=False)
def login_form( 
    *,
    db: Session = Depends(dependencies.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Rota para testes de autorização via documentação (Swagger UI).
    """
    login_data = LoginSchema(email=form_data.username, senha=form_data.password)
    
    return auth_service.login_for_access_token(db=db, login_data=login_data)

@router.get("/refresh_token", response_model=Token)
def refresh_access_token(*, current_user: Gestor | Usuario = Depends(dependencies.verificar_token)):
    """
    Gera um novo token de acesso (access_token) a partir de um token válido.
    
    Isso permite que o cliente renove seu token de acesso sem precisar
    enviar o login e a senha novamente.
    """
    return auth_service.refresh_token(current_user=current_user)



# As rotas abaixo não precisam de autenticação, então não usam a dependência no router
router_publico = APIRouter(prefix="/auth", tags=["Autenticação"])

@router_publico.post("/criar_conta", response_model=GestorResponseSchema, status_code=201)

@router_publico.post("/criar_conta", response_model=GestorResponseSchema, status_code=201)
def create_account(
    gestor_in: GestorCreateSchema,
    db: Session = Depends(dependencies.get_db)
):
    """
    Cria uma nova conta de gestor.
    """
    return auth_service.create_gestor_account(db=db, gestor_in=gestor_in)

@router_publico.post("/cadastrar_empresa", response_model=EmpresaResponseSchema, status_code=201)
def register_empresa(
    empresa_in: EmpresaCreateSchema,
    db: Session = Depends(dependencies.get_db)
):
    """
    Cadastra uma nova empresa no sistema.
    """
    return auth_service.register_empresa(db=db, empresa_in=empresa_in)