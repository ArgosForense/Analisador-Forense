from pydantic import BaseModel, Field
from beanie import PydanticObjectId

class EmpresaCreateSchema(BaseModel):
    nome: str
    cnpj: str

class EmpresaResponseSchema(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    nome: str
    cnpj: str

    class Config:
        populate_by_name = True