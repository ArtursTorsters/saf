# /api/sensors

from fastapi import APIRouter
from app.services.data_service import DataService

router = APIRouter(prefix="/api")

_data_service: DataService | None = None


def init_router(data_service: DataService) -> None:
    global _data_service
    _data_service = data_service



@router.get("/sensors")
def get_sensors():

    #all sensors with their merged metric values and type name

    if _data_service is None:
        return {"error": "Data not loaded"}, 500
    return _data_service.get_sensors()
