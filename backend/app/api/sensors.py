"""
API route for sensor data.

Single endpoint:  GET /api/sensors
Returns the merged sensor list and available metric column names.
"""

from fastapi import APIRouter

from app.services.data_service import DataService

router = APIRouter(prefix="/api")

# The DataService instance is injected from main.py at startup
_data_service: DataService | None = None


def init_router(data_service: DataService) -> None:
    """Called once at app startup to inject the loaded DataService."""
    global _data_service
    _data_service = data_service


@router.get("/sensors")
def get_sensors():
    """
    Return all sensors with their merged metric values and type names,
    plus the list of available metric column names.
    """
    if _data_service is None:
        return {"error": "Data not loaded"}, 500
    return _data_service.get_sensors()
