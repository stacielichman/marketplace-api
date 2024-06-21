import json
from typing import AsyncIterator

import httpx
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models import Base, Category
from app.schemas import CategoryCreate
from app.settings import USER, PASSWORD, HOST, PORT

TEST_POSTGRES_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/test_db"
test_engine = create_async_engine(TEST_POSTGRES_URL)
test_async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession, future=True, autoflush=False)
test_session = test_async_session()


@pytest.fixture()
async def create_db():
    async with test_session.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_session.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.mark.anyio
async def test_home(client: httpx.AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome!"}


@pytest.mark.anyio
async def test_create_category(client: httpx.AsyncClient) -> None:
    category_insert = {"title": "test_category", "description": "test_description"}
    response = await client.post("/categories/", json=category_insert)
    assert response.status_code == 200
    assert response.json() == category_insert


@pytest.mark.anyio
async def test_create_product(client: httpx.AsyncClient) -> None:
    product = {
        "title": "test_product",
        "description": "test_product_description",
        "count": 100,
        "price": 200,
    }
    response = await client.post("/products/", content=json.dumps(product),)
    assert response.status_code == 200
    assert response.json() == product


