from typing import Any
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative, Session
from sqlalchemy import select
from fastapi.exceptions import HTTPException
from fastapi import status


@as_declarative()
class Model:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class CRUDMixin:
    @classmethod
    def create(cls, db: Session, **kwargs):
        instance = cls(**kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    def update(cls, id: int, db: Session, **kwargs):
        instance = db.query(cls).filter(cls.id == id).first()
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls} not found !"
            )
        for k, v in kwargs.items():
            if v:
                setattr(instance, k, v)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    def all(cls, db: Session, skip: int = 0, limit: int = 5):
        jump = skip * limit if skip > 0 else skip
        query = select(cls).order_by("id").offset(jump).limit(limit)
        print(query)
        objects = db.execute(query).scalars().all()
        return objects

    @classmethod
    def delete(cls, id: int, db: Session):
        instance = db.query(cls).filter(cls.id == id).first()
        if instance:
            db.delete(instance)
            db.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{cls} with id {id} not found!",
            )
