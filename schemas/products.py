from db.models.product import Product, Category
from pydantic import BaseModel, Field, root_validator
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status
from db.session import get_db
from fastapi import Depends


class ProductSchema(BaseModel):
    name: str = Field(..., min_length=3)
    price_per_unit: float = Field(gt=0)
    category_id: int
