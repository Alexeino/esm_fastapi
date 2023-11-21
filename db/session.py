from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings.config import settings


SQLALCHEMY_DB_URL = settings.DATABASE_URL
print("DB_URL - ",SQLALCHEMY_DB_URL)

# Creating DB Engine
engine = create_engine(SQLALCHEMY_DB_URL)

LOCAL_SESSION = sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    try:
        db = LOCAL_SESSION()
        yield db
    finally:
        db.close()