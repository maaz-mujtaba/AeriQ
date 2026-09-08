# app/schemas.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums
class VulnerabilityGroup(str, Enum):
    ASTHMA = "asthma"
    ELDERLY = "elderly"
    RESPIRATORY = "respiratory"
    HEART_DISEASE = "heart_disease"
    CHILD = "child"
    GENERAL = "general"
    NONE = "none"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

# User schemas
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: int = Field(..., ge=1, le=120)
    gender: Gender
    city: str = Field(..., min_length=2)
    vulnerabilities: List[VulnerabilityGroup] = Field(default=[])

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    gender: str
    city: str
    vulnerabilities: List[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=1, le=120)
    gender: Optional[Gender] = None
    city: Optional[str] = Field(None, min_length=2)
    vulnerabilities: Optional[List[VulnerabilityGroup]] = None