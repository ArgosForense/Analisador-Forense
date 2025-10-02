from pydantic import BaseModel
from typing import List

class PerfilCreateSchema(BaseModel):
    nome: str
    permissoes_ids: List[int] = []

class PerfilResponseSchema(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True