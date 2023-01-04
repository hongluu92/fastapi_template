from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from api_template.db.transactional import Transactional
from api_template.errors.http_res_err import HttpResException 
from api_template.db.session import Base, session
from api_template.db.repositoies.enum import SynchronizeSessionEnum

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model : Type[ModelType] = model

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        response = await session.execute(query)
        return response.scalar_one_or_none()
    
    async def get_by_ids(
        self,
        *,
        list_ids: List[Union[int, str]],
       
    ) -> Optional[List[ModelType]]:
        response = await session.execute(
            select(self.model).where(self.model.id.in_(list_ids))
        )
        return response.scalars().all()

    async def get_multi(
        self,  offset: int = 0, limit: int = 100, 
    ) -> List[ModelType]:
        query = select(self.model).limit(limit).offset(offset)
        res = await session.execute(query)
        return res.scalars().all()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        try:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj
        except IntegrityError as ie:
            session.rollback()
            raise HttpResException("Duplicate data", "sql_duplicate", ie.args)
    
    async def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: Union[UpdateSchemaType, Dict[str, Any], ModelType],

    ) -> ModelType:

        obj_data = jsonable_encoder(obj_current)

        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.dict(
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent
        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])
    
        session.add(obj_current)
        await session.commit()
        await session.refresh(obj_current)
        return obj_current

    async def remove(
        self, *, id: Union[int, str]
    ) -> ModelType:
       
        response = await session.execute(
            select(self.model).where(self.model.id == id)
        )
        obj = response.scalar_one()
        await session.delete(obj)
        await session.commit()
        return 