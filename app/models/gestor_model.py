from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Gestor(Base):
    __tablename__ = "gestores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    senha = Column(String, nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))