from typing import Optional, Annotated
from beanie import Document, Link, Indexed
from pydantic import EmailStr, Field
from datetime import datetime
from .perfil_model import Perfil
from .gestor_model import Gestor

class Usuario(Document):
    nome: str
    # Indexed vem do beanie, unique=True cria índice único no Mongo
    email: Annotated[EmailStr, Indexed(unique=True)]
    senha: str
    status: str = "ATIVO"
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Link armazena a referência (ObjectId) para outros documentos
    perfil: Optional[Link[Perfil]] = None
    gestor: Optional[Link[Gestor]] = None 

    def desativar(self):
        if self.status == "DESATIVADO":
            return
        self.status = "DESATIVADO"

    def ativar(self):
        if self.status == "ATIVO":
            return
        self.status = "ATIVO"

    def is_ativo(self) -> bool:
        return self.status == "ATIVO"

    class Settings:
        name = "usuarios"