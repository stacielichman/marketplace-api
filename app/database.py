from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_async_engine('postgresql+asyncpg://admin:admin@localhost/postgres')
Base = declarative_base()
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
session = async_session()
