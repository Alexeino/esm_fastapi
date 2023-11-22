from db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from db.models.User import User, UserManager
from fastapi import status, exceptions


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
