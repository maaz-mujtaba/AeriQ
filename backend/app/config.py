from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Open-Meteo API
    open_meteo_base_url: str = "https://air-quality-api.open-meteo.com/v1/air-quality"
    open_meteo_timeout: int = 30  # seconds
    open_meteo_max_retries: int = 3
    
    # ML Model
    model_path: str = "./models/aqi_model.pkl"
    
    # City data
    cities_csv_path: str = "./data/city_coordinates.csv"
    
    # API
    api_prefix: str = "/api"
    
    # CORS (Frontend URLs)
    cors_origins: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create a single instance to import everywhere
settings = Settings()