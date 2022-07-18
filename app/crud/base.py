from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return await db.get(self.model, id)

    async def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        q = await db.execute(select(self.model).offset(skip).limit(limit))
        return q.scalars().all()

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        create_data = obj_in.dict(exclude_unset=True)
        db_obj = self.model(**create_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(  # pylint:disable=no-self-use
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: Session, *, obj: Union[int, ModelType]) -> None:
        if isinstance(obj, int):
            obj = await db.get(self.model, id)
        await db.delete(obj)
        await db.commit()
