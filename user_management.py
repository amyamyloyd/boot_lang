"""
User management endpoints for profile and password updates.

This module provides authenticated users the ability to:
- Update their profile (username, email)
- Change their password
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db, User
from auth_utils import hash_password, verify_password, validate_password_strength
from auth import get_current_user

router = APIRouter(prefix="/api/user", tags=["user-management"])


# Pydantic models
class ChangePasswordRequest(BaseModel):
    """Request model for changing user password."""
    current_password: str = Field(..., description="Current password for verification")
    new_password: str = Field(..., min_length=4, description="New password (minimum 4 characters)")


class UpdateProfileRequest(BaseModel):
    """Request model for updating user profile."""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="New username")
    email: Optional[str] = Field(None, max_length=100, description="New email address")


class UserResponse(BaseModel):
    """Response model for user operations."""
    success: bool
    message: str
    user: Optional[dict] = None


@router.put("/password", response_model=UserResponse)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user's password.
    
    Requires current password for verification and validates new password strength.
    
    Args:
        request: Password change request with current and new passwords
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        UserResponse: Success message
        
    Raises:
        HTTPException: If current password is incorrect or new password is invalid
    """
    # Verify current password
    if not verify_password(request.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )
    
    # Validate new password strength
    is_valid, error = validate_password_strength(request.new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    # Check if new password is same as current
    if verify_password(request.new_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password"
        )
    
    # Update password
    current_user.password_hash = hash_password(request.new_password)
    db.commit()
    
    return UserResponse(
        success=True,
        message="Password changed successfully"
    )


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile information.
    
    Users can update their username and/or email address.
    
    Args:
        request: Profile update request with new username and/or email
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        UserResponse: Success message with updated user info
        
    Raises:
        HTTPException: If username/email already exists or no changes provided
    """
    # Check if at least one field is provided
    if not request.username and not request.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (username or email) must be provided"
        )
    
    # Update username if provided
    if request.username:
        # Check if username is different
        if request.username == current_user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New username is the same as current username"
            )
        
        # Check if username already exists
        existing_user = db.query(User).filter(
            User.username == request.username,
            User.id != current_user.id
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        current_user.username = request.username
    
    # Update email if provided
    if request.email:
        # Check if email is different
        if request.email == current_user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New email is the same as current email"
            )
        
        # Check if email already exists
        existing_email = db.query(User).filter(
            User.email == request.email,
            User.id != current_user.id
        ).first()
        
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        current_user.email = request.email
    
    # Commit changes
    db.commit()
    db.refresh(current_user)
    
    return UserResponse(
        success=True,
        message="Profile updated successfully",
        user={
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "is_admin": current_user.is_admin
        }
    )

