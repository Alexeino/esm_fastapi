from pydantic import BaseModel, Field
from typing import Optional, Any


class ProductSchema(BaseModel):
    name: str = Field(..., min_length=3)
    price_per_unit: float = Field(gt=0)
    category_id: int


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    price_per_unit: Optional[float] = None
    category_id: Optional[int] = None


class CategorySchema(BaseModel):
    name: str
    category_code: str


class ProductResponseSchema(BaseModel):
    id: Any
    name: str
    price_per_unit: float
    category: Optional[CategorySchema]
