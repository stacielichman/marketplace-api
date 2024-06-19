from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, \
    Sequence, Identity, ForeignKey
from sqlalchemy.orm import relationship
from typing import Dict, Any, Text

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=True)
    phone_num = Column(String(50))


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text(280), nullable=True, index=True)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text(280), nullable=True, index=True)
    count = Column(Integer, default=0, index=True)
    price = Column(Float, default=0, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", backref="products")
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", backref="products")
