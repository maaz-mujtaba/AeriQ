from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.routes import router as api_router
from app.models import HealthCheckResponse
from app.ml_model import get_predictor
from app.cities import load_cities_from_csv, get_city_count


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    print("🚀 Starting AeriQ API...")
    
    # Load cities
    load_cities_from_csv()
    print(f"📊 Loaded {get_city_count()} cities")
    
    # Load ML model
    predictor = get_predictor()
    if predictor.is_loaded:
        print("✅ ML model loaded successfully")
    else:
        print("⚠️ No ML model found. Using CPCB formula fallback.")
    
    print("=" * 50)
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📊 City Count: {} cities available".format(get_city_count()))
    print("=" * 50)
    
    yield
    
    # Shutdown
    print("🛑 Shutting down AeriQ API...")


# Create FastAPI app
app = FastAPI(
    title="AeriQ API",
    description="Air Quality Prediction System for Indian Cities",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AeriQ API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
        "cities": f"/api/cities",
        "city_count": get_city_count()
    }


@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse()


@app.get("/api-info")
async def api_info():
    """Get API information."""
    predictor = get_predictor()
    return {
        "name": "AeriQ API",
        "version": "0.1.0",
        "endpoints": {
            "POST /api/predict": "Predict AQI for a city",
            "GET /api/predict/{city}": "Predict AQI for a city (GET)",
            "GET /api/cities": "List or search cities",
            "GET /api/cities/all": "Get all cities",
            "GET /api/city-count": "Get total city count",
            "GET /health": "Health check",
            "GET /docs": "Swagger API documentation"
        },
        "cities_count": get_city_count(),
        "model_loaded": predictor.is_loaded,
        "model_path": settings.model_path
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )