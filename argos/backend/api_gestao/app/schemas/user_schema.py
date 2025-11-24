from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from beanie import PydanticObjectId
# 1. Importe o schema do perfil para aninhar
from .perfil_schema import PerfilResponseSchema 

class UserResponseSchema(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    nome: str
    email: EmailStr
    status: str
    
    # 2. Adicionamos este campo. 
    # Como o repositório usa fetch_links=True, o Beanie preenche isso automaticamente.
    perfil: Optional[PerfilResponseSchema] = None
    
    # Mantemos perfil_id como fallback, caso o link não seja carregado
    perfil_id: Optional[PydanticObjectId] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True 

class UserCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    perfil_id: PydanticObjectId 

class UserUpdateSchema(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    perfil_id: Optional[PydanticObjectId] = None
    status: Optional[str] = None