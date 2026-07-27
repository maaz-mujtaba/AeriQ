from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ============================================
# EXISTING AQI MODELS (Keep these)
# ============================================

class CityRequest(BaseModel):
    """Request model for city-based AQI prediction."""
    city: str = Field(..., description="City name (e.g., 'delhi', 'mumbai')")
    
    class Config:
        json_schema_extra = {
            "example": {
                "city": "delhi"
            }
        }


class AQIResponse(BaseModel):
    """Response model for AQI prediction."""
    city: str = Field(..., description="City name")
    state: str = Field(..., description="State name")
    latitude: float = Field(..., description="City latitude")
    longitude: float = Field(..., description="City longitude")
    
    aqi: Optional[int] = Field(None, description="Air Quality Index (0-500)")
    aqi_category: Optional[str] = Field(None, description="AQI Category")
    aqi_color: Optional[str] = Field(None, description="AQI Color code")
    
    pm25: Optional[float] = Field(None, description="PM2.5 in µg/m³")
    pm10: Optional[float] = Field(None, description="PM10 in µg/m³")
    no2: Optional[float] = Field(None, description="NO2 in µg/m³")
    so2: Optional[float] = Field(None, description="SO2 in µg/m³")
    o3: Optional[float] = Field(None, description="O3 in µg/m³")
    co: Optional[float] = Field(None, description="CO in µg/m³")
    
    temperature: Optional[float] = Field(None, description="Temperature in °C")
    humidity: Optional[float] = Field(None, description="Relative humidity in %")
    wind_speed: Optional[float] = Field(None, description="Wind speed in m/s")
    
    timestamp: Optional[str] = Field(None, description="Data timestamp")
    prediction_source: str = Field("ml_model", description="Source of prediction")
    
    class Config:
        json_schema_extra = {
            "example": {
                "city": "Delhi",
                "state": "Delhi",
                "latitude": 28.6139,
                "longitude": 77.209,
                "aqi": 340,
                "aqi_category": "Severe",
                "aqi_color": "#8B0000",
                "pm25": 280.5,
                "pm10": 420.3,
                "no2": 85.2,
                "so2": 45.1,
                "o3": 120.6,
                "co": 2.3,
                "temperature": 32.5,
                "humidity": 65.0,
                "wind_speed": 3.2,
                "timestamp": "2026-07-19T10:00:00",
                "prediction_source": "ml_model"
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    service: str = "AeriQ Backend"
    version: str = "0.1.0"


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional details")


class CitySearchResponse(BaseModel):
    """Response for city search."""
    cities: List[dict] = Field(..., description="List of matching cities")
    total: int = Field(..., description="Total number of results")
    query: Optional[str] = Field(None, description="Search query")
    limit: Optional[int] = Field(None, description="Result limit")


class CityCountResponse(BaseModel):
    """Response for city count."""
    total_cities: int = Field(..., description="Total number of cities")
    source: str = Field("Kaggle dataset (250+ Indian cities)", description="Data source")


# ============================================
# AQI CATEGORY FUNCTION (ADD THIS!)
# ============================================

def get_aqi_category(aqi: int) -> tuple:
    """
    Get AQI category and color based on AQI value.
    
    Args:
        aqi: Air Quality Index value (0-500)
    
    Returns:
        Tuple of (category, color_hex_code)
    
    CPCB AQI Categories:
    - Good: 0-50 (Green)
    - Satisfactory: 51-100 (Light Green)
    - Moderate: 101-200 (Yellow)
    - Poor: 201-300 (Orange)
    - Very Poor: 301-400 (Red)
    - Severe: 401-500 (Maroon)
    """
    if aqi is None:
        return "Unknown", "#808080"
    
    if aqi <= 50:
        return "Good", "#00FF00"
    elif aqi <= 100:
        return "Satisfactory", "#7CFC00"
    elif aqi <= 200:
        return "Moderate", "#FFFF00"
    elif aqi <= 300:
        return "Poor", "#FFA500"
    elif aqi <= 400:
        return "Very Poor", "#FF0000"
    else:
        return "Severe", "#8B0000"


# ============================================
# NEW: Enums for Health Vulnerabilities
# ============================================

class VulnerabilityGroup(str, Enum):
    """Health vulnerability groups."""
    ASTHMA = "asthma"
    ELDERLY = "elderly"
    RESPIRATORY = "respiratory"
    HEART_DISEASE = "heart_disease"
    CHILD = "child"
    GENERAL = "general"
    NONE = "none"


class Gender(str, Enum):
    """Gender options."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


# ============================================
# NEW: User Models
# ============================================

class UserCreate(BaseModel):
    """Model for user registration."""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    age: int = Field(..., ge=1, le=120, description="Age between 1 and 120")
    gender: Gender = Field(..., description="Gender")
    city: str = Field(..., description="City of residence")
    vulnerabilities: List[VulnerabilityGroup] = Field(
        default=[],
        description="List of health vulnerabilities"
    )

    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v
    
    @validator('vulnerabilities',pre=True)
    def validate_vulnerabilities(cls,v):
        if v is None:
            return []
        if isinstance(v,list):
            return v
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "User Name",
                "email": "userh@example.com",
                "password": "SecurePass123",
                "age": 45,
                "gender": "male",
                "city": "cityName",
                "vulnerabilities": ["asthma", "heart_disease"]
            }
        }


class UserLogin(BaseModel):
    """Model for user login."""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123"
            }
        }


class UserResponse(BaseModel):
    """Model for user response (excludes password)."""
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
    """Model for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserUpdate(BaseModel):
    """Model for updating user profile."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=1, le=120)
    gender: Optional[Gender] = None
    city: Optional[str] = None
    vulnerabilities: Optional[List[VulnerabilityGroup]] = None


# ============================================
# NEW: Health Risk Assessment Models
# ============================================

class CityHealthRequest(BaseModel):
    """Request model for city health assessment."""
    city: str = Field(..., description="City to check health score for")


class HealthRiskResponse(BaseModel):
    """Response model for health risk assessment."""
    user_name: str
    user_age: int
    user_city: str
    vulnerabilities: List[str]
    
    city_name: str
    city_aqi: int
    aqi_category: str
    aqi_color: str
    
    risk_score: float
    risk_category: str
    risk_color: str
    
    home_city_aqi: int
    aqi_difference: int
    is_riskier_than_home: bool
    
    recommendations: List[str]
    medical_precautions: List[str]
    travel_advice: List[str]
    
    timestamp: str
    prediction_source: str


class CityComparisonResponse(BaseModel):
    """Response model for comparing two cities."""
    city1: str
    city1_aqi: int
    city1_category: str
    city2: str
    city2_aqi: int
    city2_category: str
    difference: int
    safer_city: str