from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, nullable=False, unique=True, index=True)
    senha = Column(String, nullable=False)
    status = Column(String, default="ATIVO")
    perfil_id = Column(Integer, ForeignKey("perfis.id"))
    gestor_id = Column(Integer, ForeignKey("gestores.id"))
    
    perfil = relationship("Perfil")

    def desativar(self):
        if self.status == "DESATIVADO":
            return
        self.status = "DESATIVADO"

    def ativar(self):
        if self.status == "ATIVO":
            return
        self.status = "ATIVO"

    def is_ativo(self) -> bool:
        return self.status == "ATIVO"