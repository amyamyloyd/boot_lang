"""
Admin endpoints for user management.

This module provides admin-only endpoints for:
- Viewing all users
- Creating new users
- Deleting users
- Resetting user passwords
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db, User
from auth_utils import hash_password, validate_password_strength
from auth import get_current_user

router = APIRouter(prefix="/api/admin", tags=["admin"])


# Dependency to check if user is admin
async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to verify current user has admin privileges.
    
    Args:
        current_user: Currently authenticated user
        
    Returns:
        User: Admin user
        
    Raises:
        HTTPException: If user is not an admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


# Pydantic models
class CreateUserRequest(BaseModel):
    """Request model for creating a user as admin."""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: str = Field(..., min_length=4, description="Password")
    email: Optional[str] = Field(None, max_length=100, description="Email address")
    is_admin: bool = Field(False, description="Whether user should have admin privileges")


class ResetPasswordRequest(BaseModel):
    """Request model for resetting a user's password."""
    new_password: str = Field(..., min_length=4, description="New password")


class UserListItem(BaseModel):
    """Model for user list item (without password)."""
    id: int
    username: str
    email: Optional[str]
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class AdminResponse(BaseModel):
    """Response model for admin operations."""
    success: bool
    message: str
    user: Optional[dict] = None
    users: Optional[List[dict]] = None


@router.get("/users", response_model=AdminResponse)
async def list_users(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    List all users in the system.
    
    Admin-only endpoint that returns all users without password information.
    
    Args:
        admin_user: Current admin user
        db: Database session
        
    Returns:
        AdminResponse: List of all users
    """
    users = db.query(User).all()
    
    user_list = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        }
        for user in users
    ]
    
    return AdminResponse(
        success=True,
        message=f"Found {len(users)} users",
        users=user_list
    )


@router.post("/users", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Create a new user as admin.
    
    Admins can create users with or without admin privileges.
    
    Args:
        request: User creation request
        admin_user: Current admin user
        db: Database session
        
    Returns:
        AdminResponse: Success message with created user info
        
    Raises:
        HTTPException: If username/email already exists or validation fails
    """
    # Validate password strength
    is_valid, error = validate_password_strength(request.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Check if email already exists (if provided)
    if request.email:
        existing_email = db.query(User).filter(User.email == request.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Create new user
    hashed_pw = hash_password(request.password)
    new_user = User(
        username=request.username,
        email=request.email,
        password_hash=hashed_pw,
        is_admin=request.is_admin
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return AdminResponse(
        success=True,
        message="User created successfully",
        user={
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "is_admin": new_user.is_admin
        }
    )


@router.delete("/users/{user_id}", response_model=AdminResponse)
async def delete_user(
    user_id: int,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete a user from the system.
    
    Admin-only endpoint. Admins cannot delete themselves.
    
    Args:
        user_id: ID of user to delete
        admin_user: Current admin user
        db: Database session
        
    Returns:
        AdminResponse: Success message
        
    Raises:
        HTTPException: If user not found or trying to delete self
    """
    # Check if user exists
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    if user_to_delete.id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Delete user
    username = user_to_delete.username
    db.delete(user_to_delete)
    db.commit()
    
    return AdminResponse(
        success=True,
        message=f"User '{username}' deleted successfully"
    )


@router.put("/users/{user_id}/reset-password", response_model=AdminResponse)
async def reset_user_password(
    user_id: int,
    request: ResetPasswordRequest,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Reset a user's password as admin.
    
    Admin-only endpoint to reset any user's password without knowing current password.
    
    Args:
        user_id: ID of user whose password to reset
        request: New password
        admin_user: Current admin user
        db: Database session
        
    Returns:
        AdminResponse: Success message
        
    Raises:
        HTTPException: If user not found or password validation fails
    """
    # Validate password strength
    is_valid, error = validate_password_strength(request.new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Reset password
    user.password_hash = hash_password(request.new_password)
    db.commit()
    
    return AdminResponse(
        success=True,
        message=f"Password reset successfully for user '{user.username}'"
    )

