# app/routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
from datetime import datetime
import json
import logging
from collections import defaultdict
import requests
from sqlalchemy.orm import Session

from app.models import (
    CityRequest, AQIResponse, get_aqi_category,
    CitySearchResponse, CityCountResponse,
    UserCreate, UserLogin, TokenResponse, UserResponse,
    HealthRiskResponse, CityHealthRequest, CityComparisonResponse,
    VulnerabilityGroup
)
from app.cities import (
    get_city_coordinates, search_cities, get_all_city_data,
    get_city_count, load_cities_from_csv
)
from app.openmeteo import fetch_air_quality, calculate_aqi_from_pm25
from app.ml_model import predict_aqi, get_predictor

# ============================================
# IMPORT FROM CRUD AND AUTH (FIXED)
# ============================================
from app.crud import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    update_user,
    delete_user,
    get_users
)
from app.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_active_user,
    verify_password,
    get_password_hash
)
from app.health_risk import calculate_health_risk, get_default_threshold
from app.database import get_db
from app.config import settings

# ============================================
# CREATE ROUTER
# ============================================

router = APIRouter()
logger = logging.getLogger(__name__)


def _prediction_from_observations(data):
    # The trained model predicts a future value from lagged observations.
    # Current readings lack that history, so use the CPCB PM2.5 sub-index.
    aqi = calculate_aqi_from_pm25(data.get("pm25"))
    return aqi, "cpcb_pm25" if aqi is not None else "unavailable"


def _predict_from_observations(data):
    return _prediction_from_observations(data)[0]


def _aqi_response(city, state, latitude, longitude, data):
    aqi, prediction_source = _prediction_from_observations(data)
    category, color = get_aqi_category(aqi)
    return AQIResponse(
        city=city, state=state, latitude=latitude, longitude=longitude, aqi=aqi,
        aqi_category=category, aqi_color=color, pm25=data.get("pm25"), pm10=data.get("pm10"),
        no2=data.get("no2"), so2=data.get("so2"), o3=data.get("o3"), co=data.get("co"),
        temperature=data.get("temperature"), humidity=data.get("humidity"),
        wind_speed=data.get("wind_speed"), timestamp=data.get("timestamp"),
        prediction_source=prediction_source
    )


@router.get("/model/status")
async def model_status():
    """Expose non-sensitive model readiness details for the forecast UI."""
    info = get_predictor().get_model_info()
    return {
        "is_loaded": info["is_loaded"],
        "model_type": info.get("model_type", "RandomForestRegressor" if info["is_loaded"] else None),
        "n_estimators": info.get("n_estimators"),
        "feature_names": info.get("feature_names") or [],
        "has_scaler": info.get("has_scaler", False),
        "fallback": "CPCB PM2.5 AQI formula",
    }


# ============================================
# EXISTING AQI ROUTES
# ============================================

@router.post("/predict", response_model=AQIResponse)
async def predict_city_aqi(request: CityRequest) -> AQIResponse:
    """Predict AQI for a given city."""
    city_data = get_city_coordinates(request.city)
    if not city_data:
        suggestions = search_cities(request.city, limit=3)
        suggestion_names = [s["name"] for s in suggestions]
        raise HTTPException(
            status_code=404,
            detail={
                "error": f"City '{request.city}' not found",
                "suggestions": suggestion_names,
                "total_cities": get_city_count()
            }
        )
    
    data = fetch_air_quality(
        latitude=city_data["lat"],
        longitude=city_data["lon"]
    )
    
    if data["pm25"] is None:
        raise HTTPException(
            status_code=503,
            detail="Unable to fetch air quality data. Please try again later."
        )
    
    predicted_aqi, prediction_source = _prediction_from_observations(data)
    
    category, color = get_aqi_category(predicted_aqi)
    
    return AQIResponse(
        city=city_data["name"],
        state=city_data["state"],
        latitude=city_data["lat"],
        longitude=city_data["lon"],
        aqi=predicted_aqi,
        aqi_category=category,
        aqi_color=color,
        pm25=data["pm25"],
        pm10=data["pm10"],
        no2=data["no2"],
        so2=data["so2"],
        o3=data["o3"],
        co=data["co"],
        temperature=data["temperature"],
        humidity=data["humidity"],
        wind_speed=data["wind_speed"],
        timestamp=data["timestamp"],
        prediction_source=prediction_source
    )


@router.get("/predict/{city}", response_model=AQIResponse)
async def predict_city_aqi_get(city: str) -> AQIResponse:
    """GET endpoint for city AQI prediction."""
    return await predict_city_aqi(CityRequest(city=city))


@router.get("/aqi/current", response_model=AQIResponse)
async def current_aqi(latitude: float = Query(..., ge=-90, le=90), longitude: float = Query(..., ge=-180, le=180)):
    """Return current AQI for a map/dashboard coordinate."""
    data = fetch_air_quality(latitude, longitude)
    if data.get("pm25") is None:
        raise HTTPException(status_code=503, detail="Current air quality data is temporarily unavailable.")
    nearest = min(get_all_city_data(), key=lambda city: (city["latitude"] - latitude) ** 2 + (city["longitude"] - longitude) ** 2, default=None)
    city, state = (nearest["name"], nearest["state"]) if nearest else ("Selected location", "")
    return _aqi_response(city, state, latitude, longitude, data)


@router.get("/aqi/forecast")
async def aqi_forecast(latitude: float = Query(..., ge=-90, le=90), longitude: float = Query(..., ge=-180, le=180)):
    """Build three daily AQI projections from Open-Meteo forecast pollutants and the configured model."""
    params = {
        "latitude": latitude, "longitude": longitude, "past_days": 1, "forecast_days": 3,
        "hourly": "pm2_5,pm10,nitrogen_dioxide,sulphur_dioxide,ozone,carbon_monoxide",
        "timezone": "auto"
    }
    try:
        response = requests.get(settings.open_meteo_base_url, params=params, timeout=settings.open_meteo_timeout)
        response.raise_for_status()
        air_payload = response.json()
        hourly = air_payload.get("hourly", {})
    except requests.RequestException as exc:
        raise HTTPException(status_code=503, detail="AQI forecast is temporarily unavailable.") from exc
    times = hourly.get("time", [])
    from zoneinfo import ZoneInfo
    local_now = datetime.now(ZoneInfo(air_payload.get("timezone", "UTC")))
    today = local_now.strftime("%Y-%m-%d")
    forecast_dates = list(dict.fromkeys(stamp[:10] for stamp in times if stamp[:10] >= today))[:3]
    fields = {"pm25": "pm2_5", "pm10": "pm10", "no2": "nitrogen_dioxide", "so2": "sulphur_dioxide", "o3": "ozone", "co": "carbon_monoxide"}
    weather_by_time = {}
    try:
        weather_response = requests.get("https://api.open-meteo.com/v1/forecast", params={"latitude": latitude, "longitude": longitude, "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m", "past_days": 1, "forecast_days": 3, "timezone": "auto"}, timeout=settings.open_meteo_timeout)
        weather_response.raise_for_status()
        weather_hourly = weather_response.json().get("hourly", {})
        weather_times = weather_hourly.get("time", [])
        weather_by_time = {stamp: {"temperature": (weather_hourly.get("temperature_2m") or [None] * len(weather_times))[i], "humidity": (weather_hourly.get("relative_humidity_2m") or [None] * len(weather_times))[i], "wind_speed": (weather_hourly.get("wind_speed_10m") or [None] * len(weather_times))[i]} for i, stamp in enumerate(weather_times)}
    except requests.RequestException:
        logger.warning("Weather forecast conditions are unavailable")
    observations = []
    current_time = local_now.strftime("%Y-%m-%dT%H:%M")
    for index, stamp in enumerate(times):
        row = {key: (hourly.get(field) or [None] * len(times))[index] for key, field in fields.items()}
        row.update(weather_by_time.get(stamp, {}))
        row["timestamp"] = stamp
        observations.append(row)

    grouped = defaultdict(list)
    for index, row in enumerate(observations):
        date = row["timestamp"][:10]
        if date not in forecast_dates or row["timestamp"] < current_time:
            continue
        prior_observations = observations[max(0, index - 24):index]
        aqi, prediction_source = get_predictor().predict_from_history(row, prior_observations)
        row["predicted_aqi"] = aqi
        row["prediction_source"] = prediction_source
        grouped[date].append(row)
    forecast = []
    forecast_fields = (*fields.keys(), "temperature", "humidity", "wind_speed")
    for day_offset, (date, rows) in enumerate(sorted(grouped.items())):
        valid = [row for row in rows if row.get("pm25") is not None]
        if not valid:
            continue
        average = {key: sum(float(row[key]) for row in valid if row.get(key) is not None) / max(1, sum(row.get(key) is not None for row in valid)) if any(row.get(key) is not None for row in valid) else None for key in forecast_fields}
        predicted_values = [row["predicted_aqi"] for row in valid if row.get("predicted_aqi") is not None]
        aqi = int(round(sum(predicted_values) / len(predicted_values))) if predicted_values else calculate_aqi_from_pm25(average["pm25"])
        source_counts = {source: sum(row.get("prediction_source") == source for row in valid) for source in ("ml_model", "cpcb_fallback")}
        prediction_source = max(source_counts, key=source_counts.get) if max(source_counts.values(), default=0) else "cpcb_fallback"
        category, color = get_aqi_category(aqi)
        forecast.append({"day": "Today" if day_offset == 0 else datetime.fromisoformat(date).strftime("%A"), "date": date, "aqi": aqi, "aqi_category": category, "aqi_color": color, "temperature": average["temperature"], "temp_high": max((r["temperature"] for r in valid if r.get("temperature") is not None), default=None), "temp_low": min((r["temperature"] for r in valid if r.get("temperature") is not None), default=None), "humidity": average["humidity"], "wind_speed": average["wind_speed"], "weather_desc": "Forecast from Open-Meteo", "trend_direction": "flat", "chance_of_improvement": None, "pollutants": {key: average[key] for key in fields}, "prediction_source": prediction_source})
    if not forecast:
        raise HTTPException(status_code=503, detail="No pollutant forecast data is available for this location right now.")
    model_info = get_predictor().get_model_info()
    return {"forecast": forecast, "latitude": latitude, "longitude": longitude, "source": "Open-Meteo + AeriQ", "prediction_method": "RandomForestRegressor" if model_info["is_loaded"] else "CPCB PM2.5 fallback", "model_loaded": model_info["is_loaded"]}


@router.get("/weather/hourly")
async def weather_hourly(latitude: float = Query(..., ge=-90, le=90), longitude: float = Query(..., ge=-180, le=180)):
    params = {"latitude": latitude, "longitude": longitude, "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation_probability,surface_pressure", "forecast_days": 3, "timezone": "auto"}
    try:
        response = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=settings.open_meteo_timeout)
        response.raise_for_status()
        hourly = response.json().get("hourly", {})
    except requests.RequestException as exc:
        raise HTTPException(status_code=503, detail="Weather forecast is temporarily unavailable.") from exc
    result = []
    for i, stamp in enumerate(hourly.get("time", [])[:72]):
        result.append({"time": stamp, "temperature": (hourly.get("temperature_2m") or [None] * 72)[i], "humidity": (hourly.get("relative_humidity_2m") or [None] * 72)[i], "wind_speed": (hourly.get("wind_speed_10m") or [None] * 72)[i], "rain_chance": (hourly.get("precipitation_probability") or [None] * 72)[i], "pressure": (hourly.get("surface_pressure") or [None] * 72)[i]})
    return {"hourly": result, "latitude": latitude, "longitude": longitude}


@router.get("/cities", response_model=CitySearchResponse)
async def list_cities(
    search: Optional[str] = Query(None, description="Search query for city name"),
    limit: int = Query(50, description="Maximum number of results", ge=1, le=250)
):
    """Get list of all supported cities or search for a specific city."""
    if search:
        results = search_cities(search, limit=limit)
        return CitySearchResponse(
            cities=results,
            total=len(results),
            query=search,
            limit=limit
        )
    else:
        cities = get_all_city_data()
        return CitySearchResponse(
            cities=cities[:limit],
            total=len(cities),
            limit=limit
        )


@router.get("/cities/all")
async def get_all_cities():
    """Get all cities with pagination support."""
    cities = get_all_city_data()
    return {
        "cities": cities,
        "total": len(cities)
    }


@router.get("/city-count", response_model=CityCountResponse)
async def city_count():
    """Get total number of cities available."""
    return CityCountResponse(
        total_cities=get_city_count(),
        source="Kaggle dataset (250+ Indian cities)"
    )


@router.get("/reload-cities")
async def reload_cities():
    """Reload cities from CSV (useful for development)."""
    from app.cities import _CITIES_CACHE
    _CITIES_CACHE = None
    load_cities_from_csv()
    return {
        "status": "reloaded",
        "total_cities": get_city_count()
    }


# ============================================
# USER AUTH ROUTES (UPDATED WITH DATABASE)
# ============================================

@router.post("/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    Returns JWT token and user data.
    """
    # Check if user exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = create_user(db, user_data)
    
    # Create access token
    access_token = create_access_token({"sub": user.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user
    )


@router.post("/auth/login", response_model=TokenResponse)
async def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login a user.
    Returns JWT token and user data.
    """
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = create_access_token({"sub": user.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user
    )


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user = Depends(get_current_active_user)
):
    """
    Get current user profile.
    Requires authentication.
    """
    return current_user


@router.put("/auth/me", response_model=UserResponse)
async def update_current_user(
    user_data: dict,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile.
    Requires authentication.
    """
    from app.schemas import UserUpdate
    update_data = UserUpdate(**user_data)
    updated_user = update_user(db, current_user.id, update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/auth/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete current user.
    Requires authentication.
    """
    success = delete_user(db, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None


# ============================================
# HEALTH RISK ROUTES
# ============================================

@router.post("/health/assess", response_model=HealthRiskResponse)
async def assess_city_health(
    request: CityHealthRequest,
    current_user = Depends(get_current_user)
):
    """
    Assess health risk for a city based on user's health profile.
    Requires authentication.
    """
    # Get user's home city AQI
    user_city = current_user.city
    try:
        vulnerabilities = json.loads(current_user.vulnerabilities or "[]")
    except (TypeError, ValueError):
        vulnerabilities = []
    home_city_data = get_city_coordinates(user_city)
    if not home_city_data:
        raise HTTPException(
            status_code=404,
            detail=f"Home city '{user_city}' not found in database"
        )
    
    # Get destination city coordinates
    dest_city_data = get_city_coordinates(request.city)
    if not dest_city_data:
        raise HTTPException(
            status_code=404,
            detail=f"City '{request.city}' not found"
        )
    
    # Fetch AQI for home city
    home_data = fetch_air_quality(
        latitude=home_city_data["lat"],
        longitude=home_city_data["lon"]
    )
    
    # Fetch AQI for destination city
    dest_data = fetch_air_quality(
        latitude=dest_city_data["lat"],
        longitude=dest_city_data["lon"]
    )
    
    # Check if we got valid data
    if home_data["pm25"] is None or dest_data["pm25"] is None:
        raise HTTPException(
            status_code=503,
            detail="Unable to fetch air quality data. Please try again later."
        )
    
    # Calculate AQI using ML model (or fallback)
    home_aqi = predict_aqi({
        "pm25": home_data["pm25"],
        "pm10": home_data["pm10"],
        "no2": home_data["no2"],
        "so2": home_data["so2"],
        "o3": home_data["o3"],
        "co": home_data["co"],
        "temperature": home_data["temperature"],
        "humidity": home_data["humidity"],
        "wind_speed": home_data["wind_speed"],
    })
    
    dest_aqi = predict_aqi({
        "pm25": dest_data["pm25"],
        "pm10": dest_data["pm10"],
        "no2": dest_data["no2"],
        "so2": dest_data["so2"],
        "o3": dest_data["o3"],
        "co": dest_data["co"],
        "temperature": dest_data["temperature"],
        "humidity": dest_data["humidity"],
        "wind_speed": dest_data["wind_speed"],
    })
    
    # Fallback to CPCB formula if ML fails
    if home_aqi is None:
        home_aqi = calculate_aqi_from_pm25(home_data["pm25"])
    if dest_aqi is None:
        dest_aqi = calculate_aqi_from_pm25(dest_data["pm25"])
    
    home_aqi = int(round(home_aqi))
    dest_aqi = int(round(dest_aqi))
    
    # Get AQI category
    dest_category, dest_color = get_aqi_category(dest_aqi)
    
    # Calculate health risk
    user_profile = {
        "age": current_user.age,
        "vulnerabilities": vulnerabilities,
        "city": user_city
    }
    
    risk_result = calculate_health_risk(
        user_profile=user_profile,
        city_aqi=dest_aqi,
        home_city_aqi=home_aqi,
        city_name=dest_city_data["name"]
    )
    
    # Build response
    return HealthRiskResponse(
        user_name=current_user.name,
        user_age=current_user.age,
        user_city=user_city.title(),
        vulnerabilities=vulnerabilities,
        city_name=dest_city_data["name"],
        city_aqi=dest_aqi,
        aqi_category=dest_category,
        aqi_color=dest_color,
        risk_score=risk_result["risk_score"],
        risk_category=risk_result["risk_category"],
        risk_color=risk_result["risk_color"],
        home_city_aqi=home_aqi,
        aqi_difference=dest_aqi - home_aqi,
        is_riskier_than_home=risk_result["is_riskier_than_home"],
        recommendations=risk_result["recommendations"].get("general", []),
        medical_precautions=risk_result["recommendations"].get("medical", []),
        travel_advice=risk_result["recommendations"].get("travel", []),
        timestamp=datetime.now().isoformat(),
        prediction_source="ml_model" if get_predictor().is_loaded else "cpcb_fallback"
    )


@router.get("/health/my-threshold")
async def get_my_threshold(current_user = Depends(get_current_user)):
    """
    Get the user's alert threshold based on their vulnerabilities.
    """
    try:
        vulnerabilities = json.loads(current_user.vulnerabilities or "[]")
    except (TypeError, ValueError):
        vulnerabilities = []
    threshold = get_default_threshold(vulnerabilities)
    return {
        "threshold": threshold,
        "vulnerabilities": vulnerabilities,
        "message": f"Your alert threshold is {threshold}. You'll be notified when AQI crosses this value."
    }


# ============================================
# CITY COMPARISON ROUTE
# ============================================

@router.get("/compare/{city1}/{city2}")
async def compare_cities(
    city1: str,
    city2: str,
    current_user = Depends(get_current_user)
):
    """
    Compare AQI between two cities.
    Requires authentication.
    """
    city1_data = get_city_coordinates(city1)
    city2_data = get_city_coordinates(city2)
    
    if not city1_data:
        raise HTTPException(404, f"City '{city1}' not found")
    if not city2_data:
        raise HTTPException(404, f"City '{city2}' not found")
    
    # Fetch AQI for both cities
    aqi1 = fetch_air_quality(city1_data["lat"], city1_data["lon"])
    aqi2 = fetch_air_quality(city2_data["lat"], city2_data["lon"])
    
    if aqi1["pm25"] is None or aqi2["pm25"] is None:
        raise HTTPException(503, "Unable to fetch data. Please try again.")
    
    dest_aqi1 = predict_aqi({
        "pm25": aqi1["pm25"],
        "pm10": aqi1["pm10"],
        "no2": aqi1["no2"],
        "so2": aqi1["so2"],
        "o3": aqi1["o3"],
        "co": aqi1["co"],
        "temperature": aqi1["temperature"],
        "humidity": aqi1["humidity"],
        "wind_speed": aqi1["wind_speed"],
    })
    dest_aqi2 = predict_aqi({
        "pm25": aqi2["pm25"],
        "pm10": aqi2["pm10"],
        "no2": aqi2["no2"],
        "so2": aqi2["so2"],
        "o3": aqi2["o3"],
        "co": aqi2["co"],
        "temperature": aqi2["temperature"],
        "humidity": aqi2["humidity"],
        "wind_speed": aqi2["wind_speed"],
    })
    
    if dest_aqi1 is None:
        dest_aqi1 = calculate_aqi_from_pm25(aqi1["pm25"])
    if dest_aqi2 is None:
        dest_aqi2 = calculate_aqi_from_pm25(aqi2["pm25"])
    
    dest_aqi1 = int(round(dest_aqi1))
    dest_aqi2 = int(round(dest_aqi2))
    
    cat1, _ = get_aqi_category(dest_aqi1)
    cat2, _ = get_aqi_category(dest_aqi2)
    
    safer = city1_data["name"] if dest_aqi1 < dest_aqi2 else city2_data["name"]
    
    return CityComparisonResponse(
        city1=city1_data["name"],
        city1_aqi=dest_aqi1,
        city1_category=cat1,
        city2=city2_data["name"],
        city2_aqi=dest_aqi2,
        city2_category=cat2,
        difference=abs(dest_aqi1 - dest_aqi2),
        safer_city=safer
    )
