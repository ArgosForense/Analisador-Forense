from pydantic import BaseModel

class EmpresaCreateSchema(BaseModel):
    nome: str
    cnpj: str

class EmpresaResponseSchema(BaseModel):
    id: int
    nome: str
    cnpj: str

    class Config:
        from_attributes = True