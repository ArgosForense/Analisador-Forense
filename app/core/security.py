from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from .config import settings
import secrets
import string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def generate_random_password(length: int = 10) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))

def generate_institutional_email(name: str, domain: str = "empresa.com") -> str:
    formatted_name = name.lower().replace(" ", ".")
    return f"{formatted_name}@{domain}"

def send_credentials_email(personal_email: str, institutional_email: str, password: str):
    # Em um projeto real, aqui você integraria com um serviço de e-mail (SendGrid, SES, etc.)
    print("--- SIMULANDO ENVIO DE E-MAIL ---")
    print(f"Para: {personal_email}")
    print("Assunto: Suas credenciais de acesso ao sistema")
    print(f"Olá, seu acesso foi criado com sucesso.")
    print(f"Email institucional: {institutional_email}")
    print(f"Senha temporária: {password}")
    print("---------------------------------")