"""
Configures the SQLAlchemy engine and session.
Connects to a MySQL database (update the connection string as needed).
"""
import os
from typing import Generator, Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Update the connection string with your MySQL credentials and database name
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, Any, None]:
    """Dependency to create a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
