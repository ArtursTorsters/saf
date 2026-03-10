"""
FastAPI application entry point.

- Creates the app instance with CORS middleware.
- Loads sensor data into memory on startup.
- Mounts the /api router.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.sensors import init_router, router as sensors_router
from app.services.data_service import DataService


# ── Lifespan: runs once when the server starts ─────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load JSON data into memory before the app starts serving."""
    data_service = DataService()
    data_service.load()
    init_router(data_service)
    print("✅ Data loaded successfully")
    yield  # App is running; when it shuts down, cleanup happens here


# ── App instance ────────────────────────────────────────────────────
app = FastAPI(
    title="SAF Sensor Dashboard API",
    description="REST API for sensor measurement data",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS — allow the Vue frontend (any origin in dev) ──────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mount API routes ────────────────────────────────────────────────
app.include_router(sensors_router)
