from pydantic import BaseModel, Field
from typing import Optional, Any, List


class ProductSchema(BaseModel):
    name: str = Field(..., min_length=3)
    price_per_unit: float = Field(gt=0)
    category_id: int
    image_url: str


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


class PageResponseSchema(BaseModel):
    items: List[Any]
    next: bool | None
    pages: int
    count: int
