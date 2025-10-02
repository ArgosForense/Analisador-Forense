#ARQUIVO BASE PARA MODELOS DE ASSOCIAÇÃO 
from sqlalchemy import Column, Integer, ForeignKey, Table
from app.core.database import Base

#TABELA ASSOCIATIVA (M:N) ENTRE PERFIS E PERMISSÕES
perfil_permissao = Table(
    "perfil_permissao",
    Base.metadata,
    Column("perfil_id", Integer, ForeignKey("perfis.id"), primary_key=True),
    Column("permissao_id", Integer, ForeignKey("permissoes.id"), primary_key=True),
)