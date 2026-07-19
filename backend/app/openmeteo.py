import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging
import time
from functools import wraps

from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Simple cache
_cache = {}
CACHE_TIMEOUT = 300  # 5 minutes


def retry_on_failure(max_retries: int = 3, delay: int = 2):
    """Decorator to retry failed API calls."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                        time.sleep(delay)
            logger.error(f"All {max_retries} attempts failed: {last_error}")
            return _empty_response()
        return wrapper
    return decorator


def fetch_air_quality(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Fetch current air quality data from Open-Meteo with caching.
    
    Args:
        latitude: City latitude
        longitude: City longitude
    
    Returns:
        Dict with current air quality data
    """
    cache_key = f"{latitude:.4f}_{longitude:.4f}"
    
    # Check cache
    if cache_key in _cache:
        cached_data, cache_time = _cache[cache_key]
        if (datetime.now() - cache_time).seconds < CACHE_TIMEOUT:
            logger.info(f"📦 Using cached data for {latitude}, {longitude}")
            return cached_data
    
    # Fetch fresh data
    data = _fetch_air_quality_raw(latitude, longitude)
    
    # Store in cache (even if empty to avoid repeated failures)
    _cache[cache_key] = (data, datetime.now())
    return data


@retry_on_failure(max_retries=3, delay=2)
def _fetch_air_quality_raw(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Raw API call without caching or retry logic.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": today,
        "end_date": today,
        "hourly": [
            "pm10",
            "pm2_5",
            "nitrogen_dioxide",
            "sulphur_dioxide",
            "ozone",
            "carbon_monoxide",
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
        ],
        "timezone": "Asia/Kolkata",
    }
    
    logger.info(f"📡 Fetching data from Open-Meteo for {latitude}, {longitude}")
    
    response = requests.get(
        settings.open_meteo_base_url,
        params=params,
        timeout=getattr(settings, 'open_meteo_timeout', 30)
    )
    response.raise_for_status()
    data = response.json()
    
    # Extract hourly data
    hourly = data.get("hourly", {})
    if not hourly:
        logger.warning("No hourly data in response")
        return _empty_response()
    
    # Get the latest hour
    time_list = hourly.get("time", [])
    if not time_list:
        logger.warning("No time data in response")
        return _empty_response()
    
    last_index = -1
    
    result = {
        "timestamp": time_list[last_index],
        "pm25": hourly.get("pm2_5", [None])[last_index],
        "pm10": hourly.get("pm10", [None])[last_index],
        "no2": hourly.get("nitrogen_dioxide", [None])[last_index],
        "so2": hourly.get("sulphur_dioxide", [None])[last_index],
        "o3": hourly.get("ozone", [None])[last_index],
        "co": hourly.get("carbon_monoxide", [None])[last_index],
        "temperature": hourly.get("temperature_2m", [None])[last_index],
        "humidity": hourly.get("relative_humidity_2m", [None])[last_index],
        "wind_speed": hourly.get("wind_speed_10m", [None])[last_index],
    }
    
    # Validate data
    result = _validate_data(result)
    
    logger.info(f"✅ Fetched data: PM2.5={result['pm25']}, AQI={calculate_aqi_from_pm25(result['pm25'])}")
    return result


def fetch_historical_data(
    latitude: float,
    longitude: float,
    days_back: int = 30
) -> pd.DataFrame:
    """
    Fetch historical air quality data for ML training.
    
    Args:
        latitude: City latitude
        longitude: City longitude
        days_back: Number of days to fetch
    
    Returns:
        DataFrame with historical data
    """
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": [
            "pm10",
            "pm2_5",
            "nitrogen_dioxide",
            "sulphur_dioxide",
            "ozone",
            "carbon_monoxide",
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
        ],
        "timezone": "Asia/Kolkata",
    }
    
    try:
        logger.info(f"📡 Fetching {days_back} days of historical data for {latitude}, {longitude}")
        
        response = requests.get(
            settings.open_meteo_base_url,
            params=params,
            timeout=60  # Historical data might take longer
        )
        response.raise_for_status()
        data = response.json()
        
        hourly = data.get("hourly", {})
        if not hourly:
            logger.warning("No hourly data in historical response")
            return pd.DataFrame()
        
        # Build DataFrame
        df = pd.DataFrame({
            "timestamp": pd.to_datetime(hourly.get("time", [])),
            "pm25": hourly.get("pm2_5", []),
            "pm10": hourly.get("pm10", []),
            "no2": hourly.get("nitrogen_dioxide", []),
            "so2": hourly.get("sulphur_dioxide", []),
            "o3": hourly.get("ozone", []),
            "co": hourly.get("carbon_monoxide", []),
            "temperature": hourly.get("temperature_2m", []),
            "humidity": hourly.get("relative_humidity_2m", []),
            "wind_speed": hourly.get("wind_speed_10m", []),
        })
        
        # Drop rows with all missing values
        df = df.dropna(how="all")
        
        logger.info(f"✅ Fetched {len(df)} historical records")
        return df
        
    except Exception as e:
        logger.error(f"❌ Error fetching historical data: {e}")
        return pd.DataFrame()


def _empty_response() -> Dict[str, Any]:
    """Return empty response structure."""
    return {
        "timestamp": datetime.now().isoformat(),
        "pm25": None,
        "pm10": None,
        "no2": None,
        "so2": None,
        "o3": None,
        "co": None,
        "temperature": None,
        "humidity": None,
        "wind_speed": None,
    }


def _validate_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate that data has all required fields."""
    required_fields = [
        "timestamp", "pm25", "pm10", "no2", "so2", "o3", "co",
        "temperature", "humidity", "wind_speed"
    ]
    
    for field in required_fields:
        if field not in data:
            data[field] = None
    
    return data


def calculate_aqi_from_pm25(pm25: float) -> Optional[int]:
    """
    Calculate AQI from PM2.5 using CPCB breakpoints.
    
    CPCB AQI Breakpoints for PM2.5 (µg/m³):
    - Good: 0-30 (AQI: 0-50)
    - Satisfactory: 31-60 (AQI: 51-100)
    - Moderate: 61-90 (AQI: 101-200)
    - Poor: 91-120 (AQI: 201-300)
    - Very Poor: 121-250 (AQI: 301-400)
    - Severe: 251+ (AQI: 401-500)
    """
    if pm25 is None or pd.isna(pm25):
        return None
    
    try:
        pm25 = float(pm25)
    except (ValueError, TypeError):
        return None
    
    if pm25 <= 30:
        return int((pm25 / 30) * 50)
    elif pm25 <= 60:
        return int(50 + ((pm25 - 30) / 30) * 50)
    elif pm25 <= 90:
        return int(100 + ((pm25 - 60) / 30) * 100)
    elif pm25 <= 120:
        return int(200 + ((pm25 - 90) / 30) * 100)
    elif pm25 <= 250:
        return int(300 + ((pm25 - 120) / 130) * 100)
    else:
        return min(500, int(400 + ((pm25 - 250) / 250) * 100))


# Utility function to clear cache
def clear_cache():
    """Clear the data cache."""
    global _cache
    _cache = {}
    logger.info("Cache cleared")