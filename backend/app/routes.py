from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

from app.models import (
    CityRequest, AQIResponse, get_aqi_category, 
    CitySearchResponse, CityCountResponse
)
from app.cities import (
    get_city_coordinates, search_cities, get_all_city_data, 
    get_city_count, load_cities_from_csv
)
from app.openmeteo import fetch_air_quality, calculate_aqi_from_pm25
from app.ml_model import predict_aqi

# Create router
router = APIRouter()


@router.post("/predict", response_model=AQIResponse)
async def predict_city_aqi(request: CityRequest) -> AQIResponse:
    """
    Predict AQI for a given city.
    
    Steps:
    1. Get city coordinates from CSV
    2. Fetch current air quality data from Open-Meteo
    3. Use ML model (or fallback) to predict AQI
    4. Return formatted response
    """
    # 1. Get city coordinates
    city_data = get_city_coordinates(request.city)
    if not city_data:
        # Try search to suggest similar cities
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
    
    # 2. Fetch data from Open-Meteo
    data = fetch_air_quality(
        latitude=city_data["lat"],
        longitude=city_data["lon"]
    )
    
    # 3. Check if we got valid data
    if data["pm25"] is None:
        raise HTTPException(
            status_code=503,
            detail="Unable to fetch air quality data. Please try again later."
        )
    
    # 4. Predict AQI (ML model if available, else fallback)
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
    
    # 5. If ML prediction failed, use CPCB formula
    if predicted_aqi is None:
        predicted_aqi = calculate_aqi_from_pm25(data["pm25"])
        prediction_source = "cpcb_fallback"
    else:
        predicted_aqi = int(round(predicted_aqi))
        prediction_source = "ml_model"
    
    # 6. Get category and color
    category, color = get_aqi_category(predicted_aqi)
    
    # 7. Build response
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
    """
    Get list of all supported cities or search for a specific city.
    """
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
    global CITIES
    from app.cities import _CITIES_CACHE
    _CITIES_CACHE = None
    load_cities_from_csv()
    return {
        "status": "reloaded",
        "total_cities": get_city_count()
    }