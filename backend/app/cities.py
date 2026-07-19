import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List, Any

CITIES_CSV_PATH = Path(__file__).parent.parent /"data"/"city_coordinates.csv"

_CITIES_CACHE = None

def load_cities_from_csv() -> Dict[str,Dict[str,Any]]:


    global _CITIES_CACHE

    if _CITIES_CACHE is not None:
        return _CITIES_CACHE
    
    if not CITIES_CSV_PATH.exists():
        print(f"⚠️ City CSV not found at {CITIES_CSV_PATH}")
        return None
    
    try:
        df = pd.read_csv(CITIES_CSV_PATH)

        df.columns = df.columns.str.strip()

        if "city" not in df.columns or "lat" not in df.columns or "lon" not in df.columns:
            print("CSV missing required columns: city, lat, lon")
            return None
        
        cities = {}
        for _, row in df.iterrows():
            city_name = str(row["city"]).strip().lower()
            cities[city_name] = {
                "name": str(row["city"]).strip(),
                "lat": float(row["lat"]),
                "lon": float(row["lon"]),
                "state": str(row.get("state","Unknown")).strip() if "state" in df.columns else "Unknown"
            }

        _CITIES_CACHE = cities
        print(f"Loaded {len(cities)} cities from {CITIES_CSV_PATH}")
        return cities
    except Exception as e:
        print("Error loading cities from CSV:")
        print("   Using fallback hardcoded cities...")
        return None
    
def get_city_coordinates(city_name : str) -> Optional[Dict[str,Any]]:

    cities = load_cities_from_csv()

    city_key = city_name.strip().lower()

    if city_key in cities:
        return cities[city_key]
    
    for key, data in cities.items():
        if city_key in key or key in city_key:
            return data
    
    return None

def search_cities(query : str, limit : int = 10) -> List[Dict[str,Any]]:

    cities = load_cities_from_csv()
    query_lower = query.strip().lower()

    results = []
    for key, data in cities.items():
        if query_lower in key or query_lower in data["name"].lower():
            results.append({
                "id" : key,
                "name" : data["name"],
                "state":data["state"],
                "latitude":data["lat"],
                "longitude":data["lon"]
            })


            if len(results) >= limit:
                break

    return results

def get_all_cities() -> List[str]:
    """Get list of all city names."""
    cities = load_cities_from_csv()
    return list(cities.keys())




def get_all_city_data() -> List[Dict[str, Any]]:
    """Get data for all cities."""
    cities = load_cities_from_csv()
    return [
        {
            "id": key,
            "name": data["name"],
            "state": data["state"],
            "latitude": data["lat"],
            "longitude": data["lon"]
        }
        for key, data in cities.items()
    ]   


    
def get_city_count() -> int:
    """Get total number of cities loaded."""
    return len(load_cities_from_csv())

CITIES = load_cities_from_csv()