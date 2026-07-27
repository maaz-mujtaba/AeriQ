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
    print("🚀 Starting AeriQ API...")
    load_cities_from_csv()
    print(f"📊 Loaded {get_city_count()} cities")
    
    predictor = get_predictor()
    if predictor.is_loaded:
        print("✅ ML model loaded successfully")
    else:
        print("⚠️ No ML model found. Using CPCB formula fallback.")
    
    print("=" * 50)
    print("📍 Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔐 Auth endpoints: /api/auth/register, /api/auth/login")
    print("❤️ Health endpoints: /api/health/assess")
    print("=" * 50)
    yield
    print("🛑 Shutting down AeriQ API...")


app = FastAPI(
    title="AeriQ API",
    description="Air Quality Prediction & Health Risk Assessment System",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to AeriQ API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "auth": "/api/auth/register",
        "cities_count": get_city_count()
    }


@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    return HealthCheckResponse()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)