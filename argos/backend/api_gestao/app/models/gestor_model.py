# argos/api_gestao/app/models/gestor_model.py
from typing import Annotated
from beanie import Document, Link, Indexed
from pydantic import EmailStr
from .empresa_model import Empresa

class Gestor(Document):
    nome: str
    email: Annotated[EmailStr, Indexed(unique=True)]
    senha: str
    empresa: Link[Empresa]

    class Settings:
        name = "gestores"