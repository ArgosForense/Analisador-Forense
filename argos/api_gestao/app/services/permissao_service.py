from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from app.repositories.permissao_repository import permissao_repository
from app.schemas.permissao_schema import PermissaoCreateSchema, PermissaoUpdateSchema
from app.models.base import perfil_permissao # Tabela de associação para verificar uso

class PermissaoService:
    
    def listar_permissoes(self, db: Session):
        return permissao_repository.get_all(db)

    def criar_permissao(self, db: Session, *, permissao_in: PermissaoCreateSchema):
        permissao_existente = permissao_repository.get_by_name(db, name=permissao_in.nome)
        if permissao_existente:
            raise HTTPException(status_code=400, detail="Permissão já existe")
        
        # Usa o create genérico do BaseRepository
        return permissao_repository.create(db, obj_in=permissao_in)

    def atualizar_permissao(self, db: Session, permissao_id: int, permissao_in: PermissaoUpdateSchema):
        permissao = permissao_repository.get(db, id=permissao_id)
        if not permissao:
            raise HTTPException(status_code=404, detail="Permissão não encontrada")
        
        # Verifica se o novo nome já existe em OUTRA permissão
        permissao_com_nome = permissao_repository.get_by_name(db, name=permissao_in.nome)
        if permissao_com_nome and permissao_com_nome.id != permissao_id:
             raise HTTPException(status_code=400, detail="Já existe uma permissão com este nome")
        
        return permissao_repository.update(db, db_obj=permissao, obj_in=permissao_in)

    def deletar_permissao(self, db: Session, permissao_id: int):
        permissao = permissao_repository.get(db, id=permissao_id)
        if not permissao:
            raise HTTPException(status_code=404, detail="Permissão não encontrada")
            
        # VERIFICAÇÃO DE SEGURANÇA:
        # Conta quantos perfis usam esta permissão na tabela associativa
        uso = db.query(perfil_permissao).filter(perfil_permissao.c.permissao_id == permissao_id).count()
        
        if uso > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Não é possível deletar. Esta permissão está em uso por {uso} perfil(is)."
            )
            
        return permissao_repository.remove(db, id=permissao_id)

permissao_service = PermissaoService()