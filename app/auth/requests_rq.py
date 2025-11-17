from app.database.db import get_session
from app.database.models import User
from sqlalchemy import select
import logging


async def get_user(username):
    async with get_session() as session:
        try:
            user = await session.scalar(select(User).where(User.username == username))
            if user:
                return user
            return None
        except Exception as e:
            logging.error(f"Ошибка в get_user: {e}")


async def create_user(username: str, hashed_password: bytes):
    async with get_session() as session:
        try:
            user = User(
                username=username,
                hashed_password=hashed_password
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
        except Exception as e:
            logging.error(f"Ошибка в create_user: {e}")
            await session.rollback()
            return None