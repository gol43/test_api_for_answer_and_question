from abc import ABC, abstractmethod
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import selectinload
from app.database.db import get_session


class AbstractRepository(ABC):
    @abstractmethod
    async def find_all():
        raise NotImplementedError
    
    @abstractmethod
    async def find_one():
        raise NotImplementedError
    
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError
    
    @abstractmethod
    async def delete_one():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, model):
        self.model = model

    async def find_all(self):
        async with get_session() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return res.scalars().all()
    
    async def find_one(self, obj):
        async with get_session() as session:
            key_filter = obj['filter_key']
            value_filter = obj['filter_value']
            stmt = select(self.model).where(getattr(self.model, key_filter) == value_filter)
            res = await session.execute(stmt)
            return res.scalar()
    
    async def add_one(self, data: dict) -> int:
        async with get_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def update_one(self, obj_id: int, data: dict) -> int:
        async with get_session() as session:
            exists = await session.execute(select(self.model).where(self.model.id == obj_id))
            if not exists.scalar():
                raise ValueError(f"Объект с id {obj_id} не найден")

            stmt = update(self.model).where(self.model.id == obj_id).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
        
    async def delete_one(self, obj_id: int):
        async with get_session() as session:
            exists = await session.execute(select(self.model).where(self.model.id == obj_id))
            if not exists.scalar():
                raise ValueError(f"Объект с id {obj_id} не найден")

            stmt = delete(self.model).where(self.model.id == obj_id)
            await session.execute(stmt)
            await session.commit()

    async def delete_one_cascade(self, obj_id: int):
        async with get_session() as session:
            obj = await session.get(self.model, obj_id)
            if not obj:
                raise ValueError(f"Объект с id {obj_id} не найден")
            await session.delete(obj)
            await session.commit()

    async def find_one_with_answers(self, question_id: int, second_model):
        async with get_session() as session:
            stmt = (
                select(self.model)
                .options(selectinload(self.model.answers).joinedload(second_model.user))
                .where(self.model.id == question_id)
            )
            res = await session.execute(stmt)
            return res.scalar_one_or_none()