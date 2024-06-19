from typing import List

from fastapi import HTTPException, FastAPI
from sqlalchemy.future import select
from starlette import status

from database import session, engine, Base
from models import Product, Category, User
from schemas import ProductResponse, ProductCreate, ProductUpdate, CategoryResponse

app = FastAPI()


@app.on_event("startup")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        async with session.begin():
            session.add_all(
                [
                    User(name="User", surname="Surname", phone_num="12345678"),
                    Category(title="devices", user_id=1, category_id=1),
                    Product(title="product one", count=5, price=9.99, user_id=1, category_id=1),
                    Product(title="product two", count=10, price=10.99, user_id=1, category_id=1)
                ]
            )
            await session.commit()


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.post('/products/', response_model=ProductResponse)
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
async def get_product(product_id: int) -> Product:
    result = await session.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@app.put("/products/{product_id}/", response_model=ProductResponse)
async def update_product(product_id: int, product_update: ProductUpdate):
    result = await session.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    for field, value in product_update.dict(exclude_unset=True).items():
        setattr(product, field, value)
    await session.commit()
    return product


@app.delete("/products/{product_id}/", response_model=dict)
async def delete_product(product_id: int):
    result = await session.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    session.delete(product)
    await session.commit()
    return {"message": "Product deleted successfully"}


@app.get("/products/filter/price/asc/", response_model=List[ProductResponse])
async def get_product() -> List[Product]:
    res = await session.execute(select(Product).order_by(Product.price).desc())
    return res.scalars().all()


@app.get("/products/filter/price/desc/", response_model=List[ProductResponse])
async def get_product() -> List[Product]:
    res = await session.execute(select(Product).order_by(Product.price).asc())
    return res.scalars().all()


@app.get("/categories/", response_model=List[CategoryResponse])
async def get_categories() -> List[Category]:
    res = await session.execute(select(Category))
    return res.scalars().all()


@app.get("/products/filter/{category_name}/", response_model=List[ProductResponse])
async def get_product(category_name: str) -> List[Product]:
    category_q = await session.query(Category.id).filter_by(name=category_name)
    product_by_cat = await session.execute(select(Product).filter(Product.category_id.in_(category_q)))
    return product_by_cat.scalars().all()
