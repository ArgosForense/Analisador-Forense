from typing import Any, Generic, Type, TypeVar
from sqlalchemy.orm import Session
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)

# CRUD genérico
class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in) -> ModelType:
        # Verifica se é um dicionário ou um modelo Pydantic
        obj_in_data = obj_in.dict() if hasattr(obj_in, 'dict') else obj_in
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in) -> ModelType:
        # 1. Converte os dados de entrada (obj_in) em um dicionário
        # exclude_unset=True é importante para não apagar campos que não foram enviados
        update_data = obj_in.dict(exclude_unset=True) if hasattr(obj_in, 'dict') else obj_in

        # 2. Atualiza os atributos do objeto do banco
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field]) # setattr atualizar obj do bd antes de fazer o commit.

        # 3. Salva as alterações
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj