from typing import Generic, TypeVar, List, Optional, Type, Union
from beanie import Document, PydanticObjectId
from pydantic import BaseModel

# Definimos que o Modelo deve ser um Documento do Beanie
ModelType = TypeVar("ModelType", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    # --- CRUD Genérico Assíncrono ---

    async def get(self, id: PydanticObjectId) -> Optional[ModelType]:
        # Busca por ID
        return await self.model.get(id)

    async def get_all(self) -> List[ModelType]:
        # Busca todos e converte para lista
        return await self.model.find_all().to_list()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        # Cria a instância e salva no Mongo
        # obj_in.model_dump() é o novo .dict() do Pydantic V2
        db_obj = self.model(**obj_in.model_dump())
        await db_obj.create()
        return db_obj

    async def update(self, id: PydanticObjectId, obj_in: Union[UpdateSchemaType, dict]) -> Optional[ModelType]:
        db_obj = await self.get(id)
        if not db_obj:
            return None
        
        # Prepara os dados de atualização
        update_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, BaseModel) else obj_in
        
        # O Beanie usa o operador $set do Mongo automaticamente ao atualizar atributos
        # Mas a forma mais robusta é usar update com dicionário
        await db_obj.update({"$set": update_data})
        
        # Retorna o objeto atualizado
        return db_obj

    async def remove(self, id: PydanticObjectId) -> bool:
        db_obj = await self.get(id)
        if not db_obj:
            return False
        await db_obj.delete()
        return True