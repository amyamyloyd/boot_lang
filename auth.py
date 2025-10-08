"""
Authentication endpoints for user registration and login.

This module provides:
- User registration with password validation
- User login with JWT token generation
- Current user information endpoint
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from database import get_db, User
from auth_utils import (
    hash_password, 
    verify_password, 
    create_access_token, 
    decode_access_token,
    validate_password_strength
)

router = APIRouter(prefix="/api/auth", tags=["authentication"])
security = HTTPBearer()


# Pydantic models for request/response
class RegisterRequest(BaseModel):
    """Request model for user registration."""
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    password: str = Field(..., min_length=4, description="Password (minimum 4 characters)")
    email: Optional[str] = Field(None, max_length=100, description="Email address (optional)")


class LoginRequest(BaseModel):
    """Request model for user login."""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class AuthResponse(BaseModel):
    """Response model for authentication endpoints."""
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[dict] = None


class UserInfo(BaseModel):
    """User information model (no sensitive data)."""
    id: int
    username: str
    email: Optional[str]
    is_admin: bool
    created_at: datetime


# Dependency to get current user from JWT token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to extract and validate current user from JWT token.
    
    Args:
        credentials: HTTP Bearer token from Authorization header
        db: Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    Args:
        request: Registration request with username, password, email
        db: Database session
        
    Returns:
        AuthResponse: Success message and JWT token
        
    Raises:
        HTTPException: If username exists or validation fails
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
        is_admin=False  # New users are not admins by default
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate JWT token
    token = create_access_token(
        data={
            "sub": str(new_user.id),
            "username": new_user.username,
            "is_admin": new_user.is_admin
        }
    )
    
    return AuthResponse(
        success=True,
        message="User registered successfully",
        token=token,
        user={
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "is_admin": new_user.is_admin
        }
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    
    Args:
        request: Login request with username and password
        db: Database session
        
    Returns:
        AuthResponse: Success message, JWT token, and user info
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by username
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Generate JWT token
    token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "is_admin": user.is_admin
        }
    )
    
    return AuthResponse(
        success=True,
        message="Login successful",
        token=token,
        user={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }
    )


@router.get("/me", response_model=UserInfo)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user's information.
    
    This is a protected endpoint that requires a valid JWT token.
    
    Args:
        current_user: Current authenticated user (from JWT token)
        
    Returns:
        UserInfo: Current user's information (no sensitive data)
    """
    return UserInfo(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_admin=current_user.is_admin,
        created_at=current_user.created_at
    )

