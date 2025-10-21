"""
Database models and initialization for Boot_Lang application.

This module defines the SQLAlchemy models and provides database
initialization functionality using SQLite.
"""

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, JSON, Index
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


class Document(Base):
    """
    Document model for uploaded files (PDFs, TXT, MD, images).
    
    Attributes:
        id: Primary key
        user_id: Foreign key to User
        filename: Original filename
        file_path: Path to stored file
        content_text: Extracted text content
        file_type: File type (pdf, txt, md, png, jpg)
        created_at: Upload timestamp
    """
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    content_text = Column(Text, nullable=True)
    file_type = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}', type='{self.file_type}')>"


class POC(Base):
    """
    POC model for generated proof-of-concept projects.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to User
        poc_id: Friendly name (e.g., "customer_feedback_analyzer")
        poc_name: Display name
        description: POC description/goal
        requirements: JSON of captured requirements
        directory: Path to POC directory
        created_at: Generation timestamp
    """
    __tablename__ = "pocs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    poc_id = Column(String(100), nullable=False, index=True)
    poc_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    requirements = Column(JSON, nullable=True)
    directory = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        Index('idx_user_poc', 'user_id', 'poc_id'),
    )
    
    def __repr__(self):
        return f"<POC(id={self.id}, poc_id='{self.poc_id}', user_id={self.user_id})>"


class POCConversation(Base):
    """
    POCConversation model for storing conversation history.
    
    Attributes:
        id: Primary key
        poc_id: Foreign key to POC (can be null if POC not yet generated)
        user_id: Foreign key to User
        conversation_history: JSON of message history
        langchain_memory: JSON of LangChain memory state
        created_at: Conversation start timestamp
    """
    __tablename__ = "poc_conversations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    poc_id = Column(Integer, nullable=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    conversation_history = Column(JSON, nullable=True)
    langchain_memory = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<POCConversation(id={self.id}, user_id={self.user_id}, poc_id={self.poc_id})>"


class POCPhase(Base):
    """
    POCPhase model for tracking implementation phases.
    
    Attributes:
        id: Primary key
        poc_id: Foreign key to POC
        phase_number: Phase number (1, 2, 3)
        phase_name: Phase name (frontend, backend, database)
        instructions_file: Path to phase instructions file
        status: Phase status (pending, in_progress, completed)
        created_at: Phase creation timestamp
    """
    __tablename__ = "poc_phases"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    poc_id = Column(Integer, nullable=False, index=True)
    phase_number = Column(Integer, nullable=False)
    phase_name = Column(String(50), nullable=False)
    instructions_file = Column(String(500), nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<POCPhase(id={self.id}, poc_id={self.poc_id}, phase={self.phase_number}, status='{self.status}')>"


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
    # Import tenant models after Base is defined
    from tenant.tenant_1.poc_idea_1.backend.models import TaskModel
    
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

