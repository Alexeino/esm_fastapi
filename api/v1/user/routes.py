from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.users import UserSchema
from db.session import get_db
from db.models.User import UserManager
from fastapi.security import OAuth2PasswordRequestForm
from api.v1.user.views import authenticate_user
from settings.Security import generate_access_token, decode_token
from settings.config import settings
from schemas.users import BearerTokenSchema
from datetime import timedelta

user_router = APIRouter()


@user_router.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db)):
    user = UserManager.create_user(user=user, db=db)
    return user


@user_router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db=db)
    access_token = generate_access_token(data={"sub": user.email})
    return BearerTokenSchema(
        access_token=access_token,
        expiry_minutes=str(settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


@user_router.get("/protected")
def protected_route(current_user: dict = Depends(decode_token)):
    return {"message": "This is protected test route!", "current_user": current_user}
