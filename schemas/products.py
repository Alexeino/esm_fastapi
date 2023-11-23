from db.models.product import Product, Category
from pydantic import BaseModel, Field, root_validator
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.exceptions import HTTPException
from fastapi import status
from db.session import get_db
from fastapi import Depends


class ProductSchema(BaseModel):
    name: str = Field(..., min_length=3)
    price_per_unit: float = Field(gt=0)
    category_id: int


class CategorySchema(BaseModel):
    name: str
    category_code: str


class ProductResponseSchema(BaseModel):
    name: str
    price_per_unit: float
    category: Optional[CategorySchema]
