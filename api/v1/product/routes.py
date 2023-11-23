from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.products import ProductSchema
from db.session import get_db
from db.models.product import Product
from schemas.base_schema import create_base_schema
from schemas.products import ProductResponseSchema
from typing import List
from api.v1.user.views import UserRole

product_router = APIRouter()


@product_router.post(
    "/add", dependencies=[Depends(UserRole(allowed_roles=["STAFF", "ADMIN"]))]
)
async def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    product = Product.create(db, **product.model_dump())

    Response = create_base_schema(
        "name", "price_per_unit"
    )  # Just playing to see if i can create response schema at response time

    return Response(name=product.name, price_per_unit=str(product.price_per_unit))


@product_router.get("/all", response_model=List[ProductResponseSchema])
async def list_products(db: Session = Depends(get_db)):
    products = Product.all(db=db)
    return products


@product_router.put(
    "/update", dependencies=[Depends(UserRole(allowed_roles=["STAFF", "ADMIN"]))]
)
async def update_product(product: ProductSchema, db: Session = Depends(get_db)):
    pass

    # TODO: logic to update product
