"""Database configuration"""

from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os


# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app/data/forgeerp.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False,  # Set to True for SQL debugging
)


def create_db_and_tables():
    """Create database and tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session

