from fastapi import APIRouter, Depends
from settings.Security import decode_token
from sqlalchemy.orm import Session
from schemas.products import ProductSchema
from db.session import get_db
from db.models.product import Product
from fastapi.exceptions import HTTPException
from fastapi import status
from schemas.base_schema import create_base_schema
from schemas.products import ProductResponseSchema
from typing import List

product_router = APIRouter()


@product_router.post("/add")
async def create_product(
    product: ProductSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(decode_token),
):
    role = current_user.get("role")
    if role not in ("STAFF", "ADMIN"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have authorization to perform this action",
        )
    product = Product.create(db, **product.model_dump())

    Response = create_base_schema(
        "name", "price_per_unit"
    )  # Just playing to see if i can create response schema at response time

    return Response(name=product.name, price_per_unit=str(product.price_per_unit))


@product_router.get("/all", response_model=List[ProductResponseSchema])
async def list_products(db: Session = Depends(get_db)):
    products = Product.all(db=db)
    return products
