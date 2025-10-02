from pydantic import BaseModel, EmailStr

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

    class Config:
        from_attributes = True