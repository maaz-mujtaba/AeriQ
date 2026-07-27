"""
Authentication logic for AeriQ.
Handles password hashing, JWT tokens, and user verification.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.models import UserCreate

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# ============================================
# IN-MEMORY USER STORE (Replace with database later)
# ============================================
# For now, we'll store users in memory
# In production, use a real database

_users_db = {}  # email -> user_data
_user_counter = 1  # Auto-increment ID


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email from in-memory store."""
    return _users_db.get(email)


def create_user(user_data: UserCreate) -> Dict[str, Any]:
    """Create a new user in the in-memory store."""
    global _user_counter
    
    # Check if user already exists
    if get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    vulnerabilities = user_data.vulnerabilities

    if vulnerabilities is None:
        vulnerabilities = []
    elif isinstance(vulnerabilities,list):
        vulnerabilities = [v.value if hasattr(v,'value') else v for v in vulnerabilities]
    else:
        vulnerabilities = []
    # Create user
    user = {
        "id": _user_counter,
        "name": user_data.name,
        "email": user_data.email,
        "password_hash": hashed_password,
        "age": user_data.age,
        "gender": user_data.gender.value if hasattr(user_data.gender, 'value') else user_data.gender,
        "city": user_data.city.lower(),
        "vulnerabilities": [v.value if hasattr(v, 'value') else v for v in user_data.vulnerabilities],
        "created_at": datetime.now(),
        "updated_at": None
    }
    
    _users_db[user_data.email] = user
    _user_counter += 1
    
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate a user by email and password."""
    user = get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return user


def create_access_token(data: Dict[str, Any]) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """Decode a JWT token."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Get the current user from the JWT token."""
    payload = decode_token(token)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_user_health_profile(user: Dict[str, Any]) -> Dict[str, Any]:
    """Get health profile for risk assessment."""
    return {
        "age": user["age"],
        "vulnerabilities": user["vulnerabilities"],
        "city": user["city"],
    }


# ============================================
# Utility Functions
# ============================================

def get_user_response(user: Dict[str, Any]) -> Dict[str, Any]:
    """Convert user dict to response format (excludes password)."""
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "age": user["age"],
        "gender": user["gender"],
        "city": user["city"],
        "vulnerabilities": user["vulnerabilities"],
        "created_at": user["created_at"],
        "updated_at": user.get("updated_at"),
    }