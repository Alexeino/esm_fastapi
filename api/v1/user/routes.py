from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.users import UserSchema
from db.session import get_db
from db.models.User import UserManager

user_router = APIRouter()

@user_router.post("/register")
def register(user:UserSchema,db:Session = Depends(get_db)):
    user = UserManager.create_user(user=user,db=db)
    return user
