from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional, List
from datetime import datetime

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
from app.ml_model import predict_aqi
from app.auth import (
    create_user, authenticate_user, create_access_token,
    get_current_user, get_user_response, get_user_by_email,
    _users_db
)
from app.health_risk import calculate_health_risk, get_default_threshold

# ============================================
# CREATE ROUTER (THIS WAS MISSING!)
# ============================================

router = APIRouter()


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
    
    predicted_aqi = predict_aqi({
        "pm25": data["pm25"],
        "pm10": data["pm10"],
        "no2": data["no2"],
        "so2": data["so2"],
        "o3": data["o3"],
        "co": data["co"],
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "wind_speed": data["wind_speed"],
    })
    
    if predicted_aqi is None:
        predicted_aqi = calculate_aqi_from_pm25(data["pm25"])
        prediction_source = "cpcb_fallback"
    else:
        predicted_aqi = int(round(predicted_aqi))
        prediction_source = "ml_model"
    
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
# NEW: AUTH ROUTES
# ============================================

@router.post("/auth/register", response_model=TokenResponse)
async def register_user(user_data: UserCreate):
    """
    Register a new user.
    Returns JWT token and user data.
    """
    user = create_user(user_data)
    access_token = create_access_token({"sub": user["email"]})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(**get_user_response(user))
    )


@router.post("/auth/login", response_model=TokenResponse)
async def login_user(login_data: UserLogin):
    """
    Login a user.
    Returns JWT token and user data.
    """
    user = authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token({"sub": user["email"]})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(**get_user_response(user))
    )


@router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Get current user profile.
    Requires authentication.
    """
    return UserResponse(**get_user_response(current_user))


@router.put("/auth/me", response_model=UserResponse)
async def update_me(
    update_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Update current user profile.
    Requires authentication.
    """
    for key, value in update_data.items():
        if value is not None and key in current_user:
            if key == "vulnerabilities":
                current_user[key] = [v.value if hasattr(v, 'value') else v for v in value]
            else:
                current_user[key] = value
    
    current_user["updated_at"] = datetime.now()
    _users_db[current_user["email"]] = current_user
    
    return UserResponse(**get_user_response(current_user))


# ============================================
# NEW: HEALTH RISK ROUTES
# ============================================

@router.post("/health/assess", response_model=HealthRiskResponse)
async def assess_city_health(
    request: CityHealthRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Assess health risk for a city based on user's health profile.
    Requires authentication.
    """
    # Get user's home city AQI
    home_city_data = get_city_coordinates(current_user["city"])
    if not home_city_data:
        raise HTTPException(
            status_code=404,
            detail=f"Home city '{current_user['city']}' not found in database"
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
        "age": current_user["age"],
        "vulnerabilities": current_user["vulnerabilities"],
        "city": current_user["city"]
    }
    
    risk_result = calculate_health_risk(
        user_profile=user_profile,
        city_aqi=dest_aqi,
        home_city_aqi=home_aqi,
        city_name=dest_city_data["name"]
    )
    
    # Build response
    return HealthRiskResponse(
        user_name=current_user["name"],
        user_age=current_user["age"],
        user_city=current_user["city"].title(),
        vulnerabilities=current_user["vulnerabilities"],
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
        prediction_source="ml_model"
    )


@router.get("/health/my-threshold")
async def get_my_threshold(current_user: dict = Depends(get_current_user)):
    """
    Get the user's alert threshold based on their vulnerabilities.
    """
    threshold = get_default_threshold(current_user["vulnerabilities"])
    return {
        "threshold": threshold,
        "vulnerabilities": current_user["vulnerabilities"],
        "message": f"Your alert threshold is {threshold}. You'll be notified when AQI crosses this value."
    }


# ============================================
# CITY COMPARISON ROUTE
# ============================================

@router.get("/compare/{city1}/{city2}")
async def compare_cities(
    city1: str,
    city2: str,
    current_user: dict = Depends(get_current_user)
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