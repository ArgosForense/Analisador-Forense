from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base, perfil_permissao
from .permissao_model import Permissao

class Perfil(Base):
    __tablename__ = "perfis"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    permissoes = relationship("Permissao", secondary=perfil_permissao)