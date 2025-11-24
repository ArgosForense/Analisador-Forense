from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId


class GestorCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    empresa_id: PydanticObjectId = Field(alias="empresa_id") # deixo assim ou empresa_id: id ?????

class GestorResponseSchema(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    nome: str
    email: EmailStr

    class Config:
        populate_by_name = True