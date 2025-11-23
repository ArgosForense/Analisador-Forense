from pydantic import BaseModel, EmailStr
from typing import Optional
from .perfil_schema import PerfilResponseSchema  

# Schema para criação de usuário (o que o gestor envia)
class UserCreateSchema(BaseModel):
    nome: str
    email: EmailStr  # Email pessoal para envio das credenciais
    perfil_id: int

# Schema de resposta (o que a API retorna)
class UserResponseSchema(BaseModel):
    id: int
    nome: str
    email: EmailStr # Email institucional
    status: str
    perfil_id: int
    
    # adicionado o objeto perfil aninhado para ler o nome dele no front
    perfil: Optional[PerfilResponseSchema] = None

    class Config:
        from_attributes = True