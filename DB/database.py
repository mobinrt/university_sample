from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import AsyncGenerator

class Database:
    DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/university"

    def __init__(self):
        self.engine = create_async_engine(self.DATABASE_URL, echo=True)
        self.async_session = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self.Base: DeclarativeMeta = declarative_base()

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session() as session:
            yield session

db = Database()
