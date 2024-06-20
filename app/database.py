from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import USER, PASSWORD, HOST, PORT, NAME

POSTGRES_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
engine = create_async_engine(POSTGRES_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
session = async_session()
