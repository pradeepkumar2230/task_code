from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Database URL - use PostgreSQL in production, SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    # For testing, fallback to SQLite if DATABASE_URL mot provided
    print("Postgresql not provided switching to sqlite")
    DATABASE_URL = "sqlite:///./medication.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
