from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core.security import get_password_hash
from app.models.gestor_model import Gestor
from app.schemas.gestor_schema import GestorCreateSchema

class GestorService:
    def create_gestor_account(self, db: Session, *, gestor_in: GestorCreateSchema) -> Gestor:
        gestor_existente = db.query(Gestor).filter(Gestor.email == gestor_in.email).first()
        if gestor_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Já existe um gestor com este e-mail."
            )
        
        hashed_password = get_password_hash(gestor_in.senha)
        db_gestor = Gestor(
            nome=gestor_in.nome,
            email=gestor_in.email,
            senha=hashed_password,
            empresa_id=gestor_in.empresa_id
        )
        db.add(db_gestor)
        db.commit()
        db.refresh(db_gestor)
        return db_gestor

gestor_service = GestorService()