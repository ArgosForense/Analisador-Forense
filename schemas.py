#OBJETIVO: Velocidade e Integridade do sistema - faz a conexão com o models.py
from pydantic import BaseModel
from typing import List, Optional

class GestorSchema(BaseModel):
    nome: str
    email: str
    senha: str
    empresa_id: int

    class Config:
        from_attributes = True
        
# Parametros necessários para o Gestor criar um novo usuário no sistema
class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    perfil_id: int
    gestor_id: int ; #Talvez não seja necessário, pois o usuário será criado pelo gestor, que já está vinculado a uma empresa específica

    class Config:
        from_attributes = True
        
class PerfilSchema(BaseModel):
    nome: str
    permissoes: str #List[str] = [] lista de permissões atribuídas ao perfil

    class Config:
        from_attributes = True