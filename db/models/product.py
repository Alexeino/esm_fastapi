from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.models.User import User
from db.base_model import Model, CRUDMixin


class Category(Model):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    category_code: str = Column(String, nullable=True)

    products = relationship("Product", back_populates="category")
    # To enable retrieve category by doing product.category


class Product(Model, CRUDMixin):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, index=True, nullable=False)
    price_per_unit: float = Column(Float, nullable=False)

    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="products")
    # To enable reverse query like retrieving all products of a category
    # by simply doing category.products

    image_url = Column(String, nullable=True)
