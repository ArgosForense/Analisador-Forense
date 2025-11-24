# argos/api_gestao/app/models/perfil_model.py
from typing import List, Annotated
from beanie import Document, Link, Indexed
from .permissao_model import Permissao

class Perfil(Document):
    nome: Annotated[str, Indexed(unique=True)]
    # Lista de Links para Permissões
    permissoes: List[Link[Permissao]] = []

    class Settings:
        name = "perfis"