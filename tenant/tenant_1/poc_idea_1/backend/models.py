from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime

# Import Base from main database module
from database import Base

class TaskModel(Base):
    """
    Task model for tenant_1 poc_idea_1
    Stores user tasks with title, description, and status
    """
    __tablename__ = "tenant_1_poc1_tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="pending", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
