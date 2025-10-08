"""
Database models and initialization for Boot_Lang application.

This module defines the SQLAlchemy models and provides database
initialization functionality using SQLite.
"""

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database configuration
DATABASE_URL = "sqlite:///./boot_lang.db"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


class User(Base):
    """
    User model for authentication and authorization.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        username: Unique username for login
        email: User's email address (optional)
        password_hash: Bcrypt hashed password
        is_admin: Boolean flag for admin privileges
        created_at: Timestamp of account creation
        updated_at: Timestamp of last profile update
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        """String representation of User object."""
        return f"<User(id={self.id}, username='{self.username}', is_admin={self.is_admin})>"


def get_db():
    """
    Dependency function to get database session.
    
    Yields a database session and ensures it's closed after use.
    Use this in FastAPI endpoints as a dependency.
    
    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    
    Yields:
        SessionLocal: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables.
    
    This function creates all tables defined in the Base metadata.
    It's safe to call multiple times - existing tables won't be modified.
    
    Example:
        python database.py  # Run this script directly to create tables
    """
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized successfully")
    print(f"✓ Database file: boot_lang.db")
    print(f"✓ Tables created: {', '.join(Base.metadata.tables.keys())}")


if __name__ == "__main__":
    """
    When run directly, initialize the database and create all tables.
    """
    print("Initializing database...")
    init_db()

