#OBJETIVO: Velocidade e Integridade do sistema - faz a conexão com o models.py
from pydantic import BaseModel
from typing import List, Optional

class EmpresaSchema(BaseModel):
    nome: str
    cnpj: str

    class Config:
        from_attributes = True

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
        
class PermissaoSchema(BaseModel):
    nome: str

    class Config:
        from_attributes = True

class PerfilSchema(BaseModel):
    nome: str
    permissoes:List[PermissaoSchema] = [] #lista de permissões atribuídas ao perfil 
    # ou permissoes_ids: List[int] = [] lista de IDs das permissões atribuídas ao perfil

    class Config:
        from_attributes = True