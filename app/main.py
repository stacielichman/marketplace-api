from typing import List

from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select
from starlette import status

from database import engine, session
from models import Base, Category, Product
from schemas import (
    CategoryCreate,
    CategoryResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.post("/categories/", response_model=CategoryResponse)
async def create_category(category_create: CategoryCreate) -> Category:
    """Post a category"""
    category = Category(**category_create.dict())
    session.add(category)
    return category


@app.post("/products/", response_model=ProductResponse)
async def create_product(product_create: ProductCreate) -> Product:
    """Post a product"""
    product = Product(**product_create.dict())
    session.add(product)
    return product


@app.get("/products/", response_model=List[ProductResponse])
async def get_product() -> List[Product]:
    """Get all products"""
    res = await session.execute(select(Product))
    return res.scalars().all()


@app.get("/products/{product_id}/", response_model=ProductResponse)
async def get_product_by_id(product_id: int) -> Product:
    """Get product by its id"""
    result = await session.execute(
        select(Product).filter(Product.id == product_id)
    )
    product = result.scalars().first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@app.put("/products/{product_id}/", response_model=ProductResponse)
async def update_product(product_id: int, product_update: ProductUpdate):
    """Update a product by its id"""
    result = await session.execute(
        select(Product).filter(Product.id == product_id)
    )
    product = result.scalars().first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    for field, value in product_update.dict(exclude_unset=True).items():
        setattr(product, field, value)
    await session.commit()
    return product


@app.delete("/products/{product_id}/", response_model=dict)
async def delete_product(product_id: int):
    """Delete a product by its id"""
    result = await session.execute(
        select(Product).filter(Product.id == product_id)
    )
    product = result.scalars().first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    session.delete(product)
    await session.commit()
    return {"message": "Product deleted successfully"}


@app.get("/products/filter/price/asc/", response_model=List[ProductResponse])
async def filter_product_by_price_asc() -> List[Product]:
    """Get products filtered by ascending price"""
    res = await session.execute(select(Product).order_by(Product.price.asc()))
    return res.scalars().all()


@app.get("/products/filter/price/desc/", response_model=List[ProductResponse])
async def filter_product_by_price_desc() -> List[Product]:
    """Get products filtered by descending price"""
    res = await session.execute(select(Product).order_by(Product.price.desc()))
    return res.scalars().all()


@app.get("/categories/", response_model=List[CategoryResponse])
async def get_categories() -> List[Category]:
    """Get all categories"""
    res = await session.execute(select(Category))
    return res.scalars().all()


@app.get(
    "/products/filter/{category_name}/",
    response_model=List[ProductResponse]
)
async def filter_product_by_category(category_name: str) -> List[Product]:
    category_q = await session.execute(
        select(Category.id).filter_by(title=category_name)
    )
    category_ids = category_q.scalars().all()
    product_by_cat = await session.execute(
        select(Product).filter(Product.category_id.in_(category_ids))
    )
    return product_by_cat.scalars().all()
