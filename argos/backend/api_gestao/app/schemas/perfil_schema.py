from pydantic import BaseModel
from typing import List, Optional
from beanie import PydanticObjectId
from pydantic import Field

class PerfilCreateSchema(BaseModel):
    nome: str
    permissoes_ids: List[PydanticObjectId] 

class PerfilResponseSchema(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    nome: str
    # Retornamos os objetos de permissão aninhados ou apenas IDs, depende da sua View
    # Aqui vou deixar simplificado

    class Config:
        populate_by_name = True