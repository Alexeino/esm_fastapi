from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from settings.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def generate_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    ),
):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def decode_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise credentials_exception
