from pydantic import BaseModel, EmailStr

class GestorCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    empresa_id: int

class GestorResponseSchema(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True