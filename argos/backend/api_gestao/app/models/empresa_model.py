# argos/api_gestao/app/models/empresa_model.py
from beanie import Document, Indexed

class Empresa(Document):
    nome: str
    cnpj: str = Indexed(unique=True)

    class Settings:
        name = "empresas"