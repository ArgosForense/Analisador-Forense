from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from beanie import PydanticObjectId

# Schema de Retorno (Response)
class UserResponseSchema(BaseModel):
    # O alias='_id' ajuda o Pydantic a ler o campo _id do Mongo e jogar para id
    id: PydanticObjectId = Field(alias="_id")
    nome: str
    email: EmailStr
    status: str
    
    # Perfil agora é opcional e pode ser retornado como ID ou Objeto
    # Para simplificar, retornamos o ID do perfil se ele estiver linkado
    perfil_id: Optional[PydanticObjectId] = None
    
    class Config:
        # Permite popular o schema a partir de um objeto Beanie
        from_attributes = True
        # Garante que o ObjectId seja convertido para string no JSON final
        populate_by_name = True 

# Schema de Criação (Request)
class UserCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    # Recebemos o ID do perfil como string/ObjectId
    perfil_id: PydanticObjectId 

# Schema de Edição
class UserUpdateSchema(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    perfil_id: Optional[PydanticObjectId] = None
    status: Optional[str] = None