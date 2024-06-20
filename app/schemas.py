from pydantic import BaseModel


class ProductCreate(BaseModel):
    title: str
    description: str
    count: int
    price: float


class ProductUpdate(BaseModel):
    count: int
    description: str
    price: float


class ProductResponse(BaseModel):
    title: str
    description: str
    count: int
    price: float

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    title: str
    description: str


class CategoryResponse(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True
