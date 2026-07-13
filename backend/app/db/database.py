from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflus = False,
    bind = engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()