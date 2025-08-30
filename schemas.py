#OBJETIVO: Velocidade e Integridade do sistema
from pydantic import BaseModel
from typing import List, Optional

class GestorSchema(BaseModel):
    nome: str
    email: str
    senha: str
    empresa_id: int

    class Config:
        from_attributes = True