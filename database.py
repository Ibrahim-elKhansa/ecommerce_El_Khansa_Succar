from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./database.db"

"""
Module: database

This module configures and initializes the database connection for the application.
It defines the SQLAlchemy engine, session, and declarative base for database models.

Configuration:
    - DATABASE_URL: Specifies the path to the SQLite database.
    - `engine`: SQLAlchemy engine for connecting to the SQLite database.
    - `SessionLocal`: Configured sessionmaker instance for database sessions.
    - `Base`: Declarative base class for defining database models.

Functions:
    - get_db(): Provides a database session for FastAPI dependency injection.
      Ensures proper session lifecycle management (creation and closure).

Usage:
    - Import `Base` to define database models in the application.
    - Use `get_db` in FastAPI routes to interact with the database.
"""


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency function to provide a database session.

    This function is used in FastAPI dependency injection to ensure that a 
    database session is created and properly closed after usage.

    Yields:
        SessionLocal: A database session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
