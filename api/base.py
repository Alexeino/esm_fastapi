from fastapi import APIRouter
from api.v1.user.routes import user_router
from api.v1.product.routes import product_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(product_router, prefix="/product", tags=["product"])
