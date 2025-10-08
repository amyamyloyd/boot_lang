"""
Authentication utilities for JWT token management and password hashing.

This module provides functions for:
- Password hashing and verification using bcrypt
- JWT token creation and validation
- Token payload extraction
"""

import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
import os

# JWT Configuration
# In production, load these from environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        str: Bcrypt hashed password (UTF-8 decoded string)
        
    Example:
        hashed = hash_password("mypassword123")
        # Returns: "$2b$12$..."
    """
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a bcrypt hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hashed password to compare against
        
    Returns:
        bool: True if password matches, False otherwise
        
    Example:
        is_valid = verify_password("mypassword123", stored_hash)
        if is_valid:
            print("Password correct!")
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Dictionary of data to encode in the token (usually user_id, username)
        expires_delta: Optional custom expiration time delta
        
    Returns:
        str: Encoded JWT token
        
    Example:
        token = create_access_token(
            data={"sub": "user123", "username": "john", "is_admin": False}
        )
        # Returns: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    
    to_encode.update({"exp": expire})
    
    # Create and return JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT access token.
    
    Args:
        token: JWT token string to decode
        
    Returns:
        Optional[Dict]: Decoded token payload if valid, None if invalid or expired
        
    Example:
        payload = decode_access_token(token)
        if payload:
            user_id = payload.get("sub")
            username = payload.get("username")
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password meets minimum requirements.
    
    Requirements:
    - Minimum 4 characters
    
    Args:
        password: Password string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: Optional[str])
        
    Example:
        is_valid, error = validate_password_strength("pass")
        if not is_valid:
            print(f"Password error: {error}")
    """
    if len(password) < 4:
        return False, "Password must be at least 4 characters long"
    
    return True, None

