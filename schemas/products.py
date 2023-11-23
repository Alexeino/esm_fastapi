from pydantic import BaseModel, Field
from typing import Optional


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
