from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer # cria a estrutura de tokens bearer
from dotenv import load_dotenv
import os

load_dotenv() 

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_schema = OAuth2PasswordBearer(tokenUrl="auth/login") # !!!! eh necessario para passar o token como um header ao inves do body na requisição !!!! temporário

# Roteadores
from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# para rodar o código, executar no terminal: uvicorn main:app --reload