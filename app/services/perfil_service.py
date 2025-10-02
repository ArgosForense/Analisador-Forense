from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.perfil_model import Perfil, Permissao
from app.schemas.perfil_schema import PerfilCreateSchema

class PerfilService:
    def criar_perfil(self, db: Session, *, perfil_in: PerfilCreateSchema) -> Perfil:
        # 1. Busca os objetos de Permissao com base nos IDs recebidos
        permissoes_encontradas = db.query(Permissao).filter(Permissao.id.in_(perfil_in.permissoes_ids)).all()
        
        # 2. Validação de negócio: verificar se todos os IDs fornecidos existem
        if len(permissoes_encontradas) != len(perfil_in.permissoes_ids):
            raise HTTPException(status_code=400, detail="Uma ou mais permissões não foram encontradas.")
            
        # 3. Cria o novo perfil
        db_obj = Perfil(nome=perfil_in.nome, permissoes=permissoes_encontradas)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

perfil_service = PerfilService()