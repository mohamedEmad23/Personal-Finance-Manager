from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from .config import get_settings

settings = get_settings()

engine = create_engine(
    settings.MYSQL_URI,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
