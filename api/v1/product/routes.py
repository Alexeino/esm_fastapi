from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.product import Product
from schemas.base_schema import create_base_schema
from schemas.products import ProductResponseSchema, ProductSchema, ProductUpdateSchema
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
async def list_products(page: int = 1, limit: int = 5, db: Session = Depends(get_db)):
    skip = page - 1 if page > 0 else page
    products = Product.all(db=db, skip=skip, limit=limit)
    return products


@product_router.put(
    "/update",
    dependencies=[Depends(UserRole(allowed_roles=["STAFF", "ADMIN"]))],
    response_model=ProductResponseSchema,
)
async def update_product(
    id: int, product: ProductUpdateSchema, db: Session = Depends(get_db)
):
    updated_product = Product.update(id=id, db=db, **product.model_dump())
    return updated_product
