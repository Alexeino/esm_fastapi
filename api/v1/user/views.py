from db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from db.models.User import User, UserManager
from fastapi import status, exceptions
from settings.Security import decode_token


def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    return user


def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(email=email, db=db)
    if not user:
        raise exceptions.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with provided email not found!",
        )
    if not UserManager.verify_password(password, user.password):
        raise exceptions.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password Incorrect"
        )
    return user


class UserRole:
    def __init__(self, allowed_roles: list[str] = ["STAFF"]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: dict = Depends(decode_token)):
        role = current_user.get("role")
        if role not in self.allowed_roles:
            raise exceptions.HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have authorization to perform this action",
            )
        return current_user
