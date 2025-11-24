from pydantic import BaseModel
from beanie import PydanticObjectId
from pydantic import Field

class PermissaoCreateSchema(BaseModel):
    nome: str

class PermissaoUpdateSchema(BaseModel):
    nome: str

class PermissaoResponseSchema(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    nome: str

    class Config:
        populate_by_name = True
        