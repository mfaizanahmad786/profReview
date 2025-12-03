"""
Database Connection Setup
This file configures SQLAlchemy to connect to PostgreSQL.
It provides:
- Engine: The connection to the database
- SessionLocal: A factory for creating database sessions
- Base: The base class all models will inherit from
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create the database engine
# echo=True logs all SQL statements (helpful for debugging)
engine = create_engine(settings.DATABASE_URL, echo=True)

# SessionLocal is a factory for creating database sessions
# A session is like a "workspace" for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class for all our database models
Base = declarative_base()


def get_db():
    """
    Dependency function that provides a database session to route handlers.
    The session is automatically closed after the request completes.
    
    Usage in routes:
        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            # db is now available here
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

