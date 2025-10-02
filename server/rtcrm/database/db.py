import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

database_url = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@host.docker.internal:5432/rtcrm")
# database_url = "postgresql+psycopg://postgres:postgres@host.docker.internal:5432/rtcrm"

class Base(DeclarativeBase):
    pass

engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
