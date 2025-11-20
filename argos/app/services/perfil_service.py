from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from app.models.perfil_model import Perfil, Permissao
from app.schemas.perfil_schema import PerfilCreateSchema
from app.repositories.perfil_respository import perfil_repository

class PerfilService:
    
    def listar_perfis(self, db: Session) -> List[Perfil]:
        """Retorna a lista de todos os perfis."""
        return perfil_repository.get_all(db)
    
    def criar_perfil(self, db: Session, *, perfil_in: PerfilCreateSchema) -> Perfil:
        # 1. Busca os objetos de Permissao com base nos IDs recebidos
        permissoes_encontradas = db.query(Permissao).filter(Permissao.id.in_(perfil_in.permissoes_ids)).all()
        
        # 2. Validação de negócio: verificar se todos os IDs fornecidos existem
        if len(permissoes_encontradas) != len(perfil_in.permissoes_ids):
            raise HTTPException(status_code=400, detail="Uma ou mais permissões não foram encontradas.")
            
        # 3. Cria o novo perfil
        # db_obj = Perfil(nome=perfil_in.nome, permissoes=permissoes_encontradas)
        # db.add(db_obj)
        # db.commit()
        # db.refresh(db_obj)
        # return db_obj
        
        
        # ajuste 3. Cria o novo perfil usando o repositório (que encapsula a lógica do DB)
        return perfil_repository.create_with_permissions(db, nome=perfil_in.nome, permissoes=permissoes_encontradas)

perfil_service = PerfilService()