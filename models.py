from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

# Criação da conexão com o banco de dados
db = create_engine("sqlite:///banco_test.db")

# Cria a base para criação dos modelos
Base = declarative_base()

# criar as classes/tabelas do banco de dados
# Empresa possui gestores, estes cadastram usuários e cada usuário é atribuido a um perfil com permissões definidas pelo gestor
# 1.TipoUsuario

 

class Empresa(Base):
    __tablename__ = "empresas"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    cnpj = Column("cnpj", String, nullable=False)
    
    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj
        
class Gestor(Base):
    __tablename__ = "gestores"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    empresa_id = Column("empresa_id", Integer, ForeignKey("empresas.id")) # 1 empresa possui vários gestores, mas 1 gestor pertence a apenas 1 empresa
    
    def __init__(self, nome, email, senha, empresa_id):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.empresa_id = empresa_id
        
        
class Usuario(Base):
    __tablename__ = "usuarios"
    
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    status = Column("status", String) # ATIVO ou DESATIVADO
    perfil_id = Column("perfil_id", Integer, ForeignKey("perfis.id")) # 1 usuário possui 1 perfil, mas 1 perfil pode ser vinculado a vários usuários
    gestor_id = Column("gestor_id", Integer, ForeignKey("gestores.id")) # 1 gestor pode criar vários usuários, mas 1 usuário é criado por apenas 1 gestor
    
    def __init__(self, nome, email, senha, perfil_id, gestor_id, status="ATIVO"):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.perfil_id = perfil_id
        self.gestor_id = gestor_id
        self.status = status
        
class Permissao(Base):
    __tablename__ = "permissoes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)

#Uso do objeto Table para criar essa associação, pois ele é mais leve e direto para esse propósito. Só criamos uma classe se a tabela de associação tiver campos adicionais (como data de criação, status, etc).    
perfil_permissao = Table(
    "perfil_permissao",
    Base.metadata,
    Column("perfil_id", Integer, ForeignKey("perfis.id")),
    Column("permissao_id", Integer, ForeignKey("permissoes.id"))
)

class Perfil(Base):
    __tablename__ = "perfis"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    permissoes = relationship("Permissao", secondary=perfil_permissao, backref="perfis")
    
    def __init__(self, nome, permissoes):
        self.nome = nome
        self.permissoes = permissoes
        
# executa a criação dos metadados do banco (criação efetiva do banco)
