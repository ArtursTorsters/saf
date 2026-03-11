# loads data in memory and get api
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.sensors import init_router, router as sensors_router
from app.services.data_service import DataService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # json load in memory
    data_service = DataService()
    data_service.load()
    init_router(data_service)
    print("✅ Data loaded successfully")
    yield


app = FastAPI(
    title="SAF Sensor Dashboard API",
    description="REST API for sensor measurement data",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensors_router)
