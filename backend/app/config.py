from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Open-Meteo API
    open_meteo_base_url: str = "https://air-quality-api.open-meteo.com/v1/air-quality"
    open_meteo_timeout: int = 30
    
    # ML Model
    model_path: str = "./models/aqi_model.pkl"
    
    # City data
    cities_csv_path: str = "./data/city_coordinates.csv"
    
    # API
    api_prefix: str = "/api"
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    
    # ==========================================
    # NEW: Authentication Settings
    # ==========================================
    # Secret key for JWT tokens (CHANGE THIS IN PRODUCTION!)
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 hours
    
    # ==========================================
    # NEW: Alert Thresholds by Vulnerability Group
    # ==========================================
    alert_thresholds: dict = {
        "asthma": 50,
        "elderly": 50,
        "respiratory": 50,
        "heart_disease": 50,
        "child": 50,
        "general": 100
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()