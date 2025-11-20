from sqlalchemy.orm import Session
from typing import List

from app.models.perfil_model import Perfil
from app.models.permissao_model import Permissao

class PerfilRepository:
    def get_by_name(self, db: Session, *, nome: str) -> Perfil | None:
        """
        Busca um perfil pelo nome.
        """
        return db.query(Perfil).filter(Perfil.nome == nome).first()

    def get_all(self, db: Session) -> List[Perfil]:
        """
        Busca todos os perfis cadastrados.
        """
        return db.query(Perfil).all()

    def create_with_permissions(self, db: Session, *, nome: str, permissoes: List[Permissao]) -> Perfil:
        """
        Cria um novo objeto Perfil no banco de dados, já associando as permissões.
        """
        # Cria a instância do modelo Perfil
        db_perfil = Perfil(nome=nome, permissoes=permissoes)
        
        # Adiciona à sessão, commita e atualiza a instância com os dados do banco (como o ID)
        db.add(db_perfil)
        db.commit()
        db.refresh(db_perfil)
        
        return db_perfil

# Cria uma instância única do repositório para ser usada em toda a aplicação

#perfil_repository = PerfilRepository(Perfil)
perfil_repository = PerfilRepository()