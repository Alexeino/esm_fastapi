from fastapi import APIRouter
from api.v1.user import routes

api_router = APIRouter()

api_router.include_router(routes.user_router,prefix="/user",tags=["user"])