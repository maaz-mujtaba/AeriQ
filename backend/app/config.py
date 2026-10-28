# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # ============================================
    # OPEN-METEO API
    # ============================================
    open_meteo_base_url: str = "https://air-quality-api.open-meteo.com/v1/air-quality"
    open_meteo_timeout: int = 30
    
    # ============================================
    # ML MODEL
    # ============================================
    model_path: str = "./models/aqi_model.pkl"
    
    # ============================================
    # CITY DATA
    # ============================================
    cities_csv_path: str = "./data/city_coordinates.csv"
    
    # ============================================
    # API
    # ============================================
    api_prefix: str = "/api"
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://aeriq-one.vercel.app",
    ]
    alert_thresholds: dict = {
        "general": 100, "asthma": 75, "respiratory": 75,
        "heart_disease": 75, "elderly": 75, "child": 75,
    }
    
    # ============================================
    # DATABASE (ADD THIS!)
    # ============================================
    database_url: str = "sqlite:///./aeriq.db"
    
    # ============================================
    # JWT AUTHENTICATION (ADD THIS!)
    # ============================================
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        # Allow extra fields in .env file (they'll be ignored)
        extra = "ignore"


settings = Settings()
