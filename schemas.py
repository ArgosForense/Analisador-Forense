#OBJETIVO: Velocidade e Integridade do sistema, classe que permite padronizar a forma como irá receber as informações - faz a conexão com o models.py
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
    senha: str # ALTERAR, O GESTOR NÃO DEVE SABER A SENHA DO USUÁRIO, ELA DEVE SER GERADA AUTOMATICAMENTE E ENVIADA POR EMAIL !!!! temporário
    perfil_id: int
    gestor_id: int ; # o gestor que está criando o usuário, não faz sentido o gestor ter que informar seu id para criar o usuário !!!! temporário

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True
        
class PermissaoSchema(BaseModel):
    nome: str

    class Config:
        from_attributes = True

class PerfilSchema(BaseModel):
    nome: str
    permissoes:List[PermissaoSchema] = [] #lista de permissões atribuídas ao perfil 
    

    class Config:
        from_attributes = True