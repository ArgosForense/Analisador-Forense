from pydantic import BaseModel

class PermissaoCreateSchema(BaseModel):
    nome: str

class PermissaoResponseSchema(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True