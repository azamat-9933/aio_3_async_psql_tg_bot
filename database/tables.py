import asyncio
from sqlalchemy import URL, BigInteger
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.orm import declarative_base
from datetime import datetime

from configs import (DB_NAME, DB_USER, DB_HOST, DB_PASSWORD, DB_DRIVER)

url = URL.create(
    drivername=DB_DRIVER,
    username=DB_USER,
    host=DB_HOST,
    database=DB_NAME,
    password=DB_PASSWORD
)

engine = create_async_engine(url, echo=True)

Base = declarative_base()


class TgBotUser(Base):
    __tablename__ = "telegram_users"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger())
    language = Column(String(2), default='no')
    full_name = Column(String(255), default=None)
    phone = Column(String(255), default=None)
    status = Column(Boolean, default=False)
    joined_at = Column(DateTime(), default=datetime.now())



async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Запуск асинхронного кода

if __name__ == "__main__":
    asyncio.run(init_db())