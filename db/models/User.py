from db.base_model import Model
from sqlalchemy import Column, String, Integer, Boolean
from pydantic import EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from schemas.users import UserSchema
from fastapi.exceptions import HTTPException
from fastapi import status


class User(Model):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String, nullable=True)
    email: EmailStr = Column(String, nullable=False)
    password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean, default=True)
    is_superuser: bool = Column(Boolean, default=False)


class UserManager:
    """A Manager class to manage user creation for admin or non admin users"""

    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def create_user(cls, user: UserSchema, db: Session, superuser=False):
        db_user = User(
            email=user.email,
            is_active=user.is_active,
            is_superuser=superuser,
            username=user.username,
            password=cls.hash_password(user.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def create_superuser(cls, user: UserSchema, db: Session):
        return cls.create_superuser(user=user, db=db, superuser=True)

    @staticmethod
    def hash_password(password):
        return UserManager.context.hash(password)

    @classmethod
    def set_password(cls, user: UserSchema):
        if user:
            user.password = cls.hash_password(user.password)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Password None"
            )

    @staticmethod
    def verify_password(plain_pwd, hashed_pwd):
        return UserManager.context.verify(plain_pwd, hashed_pwd)
