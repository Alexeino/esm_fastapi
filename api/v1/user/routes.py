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
from api.v1.misc.Email import send_email_async, send_email_sync
from time import perf_counter
from api.v1.misc.base_schema import create_base_schema

user_router = APIRouter()


@user_router.post("/register")
async def register(user: UserSchema, db: Session = Depends(get_db)):
    user = UserManager.create_user(user=user, db=db)
    if user:
        await send_email_async(
            f"User Registration Succesful!",
            user.email,
            f"User {user.username} has been created!",
        )
    Response = create_base_schema("username", "email")
    return Response(username=user.username, email=user.email)


@user_router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db=db)
    access_token = generate_access_token(data={"sub": user.email, "role": user.role})
    return BearerTokenSchema(
        access_token=access_token,
        expiry_minutes=str(settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


@user_router.get("/protected")
async def protected_route(current_user: dict = Depends(decode_token)):
    start = perf_counter()
    print("Sending Email Async")
    await send_email_async("Testing Email Async", "test01@gmail.com", "Async Email")
    end = perf_counter()
    print("elapsed time - ", end - start)  # elapsed time -  0.017749178998201387
    return {"message": "This is protected test route!", "current_user": current_user}
