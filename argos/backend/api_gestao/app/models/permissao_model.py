from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Permissao(Base):
    __tablename__ = "permissoes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)