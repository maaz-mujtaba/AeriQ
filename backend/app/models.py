from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


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
    
    # AQI
    aqi: Optional[int] = Field(None, description="Air Quality Index (0-500)")
    aqi_category: Optional[str] = Field(None, description="AQI Category")
    aqi_color: Optional[str] = Field(None, description="AQI Color code")
    
    # Pollutant values
    pm25: Optional[float] = Field(None, description="PM2.5 in µg/m³")
    pm10: Optional[float] = Field(None, description="PM10 in µg/m³")
    no2: Optional[float] = Field(None, description="NO2 in µg/m³")
    so2: Optional[float] = Field(None, description="SO2 in µg/m³")
    o3: Optional[float] = Field(None, description="O3 in µg/m³")
    co: Optional[float] = Field(None, description="CO in µg/m³")
    
    # Weather
    temperature: Optional[float] = Field(None, description="Temperature in °C")
    humidity: Optional[float] = Field(None, description="Relative humidity in %")
    wind_speed: Optional[float] = Field(None, description="Wind speed in m/s")
    
    # Metadata
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


# Aliases for backward compatibility
City = CityRequest  # If your routes use "City" instead of "CityRequest"