from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.empresa_model import Empresa
from app.schemas.empresa_schema import EmpresaCreateSchema

class EmpresaService:
    def register_empresa(self, db: Session, *, empresa_in: EmpresaCreateSchema) -> Empresa:
        empresa_existente = db.query(Empresa).filter(Empresa.cnpj == empresa_in.cnpj).first()
        if empresa_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Já existe uma empresa com este CNPJ."
            )
            
        db_empresa = Empresa(nome=empresa_in.nome, cnpj=empresa_in.cnpj)
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
        return db_empresa

empresa_service = EmpresaService()