from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
import secrets
import string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def gerar_hash_senha(password: str) -> str:
    return pwd_context.hash(password)

# Padronizando para receber 'subject' (o ID do usuário)
def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None, additional_claims: dict = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # O 'sub' é o padrão JWT para o ID do usuário
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # Adiciona dados extras (como 'tipo': 'gestor')
    if additional_claims:
        to_encode.update(additional_claims)
        
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def gerar_senha_aleatoria(length: int = 10) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))

def gerar_email_institucional(name: str, domain: str = "argos.com") -> str:
    formatted_name = name.lower().replace(" ", ".")
    return f"{formatted_name}@{domain}"

def enviar_email_credenciais(personal_email: str, institutional_email: str, password: str):
    print(f"\n📨 [MOCK EMAIL] Para: {personal_email}")
    print(f"   Assunto: Credenciais Argos")
    print(f"   Login: {institutional_email} | Senha: {password}\n")