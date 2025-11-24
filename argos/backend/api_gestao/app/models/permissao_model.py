# argos/api_gestao/app/models/permissao_model.py
from beanie import Document, Indexed

class Permissao(Document):
    nome: str = Indexed(unique=True)

    class Settings:
        name = "permissoes"