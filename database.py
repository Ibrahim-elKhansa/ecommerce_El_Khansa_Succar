from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./database.db"

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
