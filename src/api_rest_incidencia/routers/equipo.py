from fastapi import APIRouter, Request, requests, status
from api_rest_incidencia.database import equipo
from api_rest_incidencia.models.equipo import Equipo

router = APIRouter(
    prefix="/equipos",
    tags=["equipos"]
)

def get_handdler(request:Request) -> equipo.HanddlerEquipoDB:
    return request.app.state.handdler_equipo_db

@router.post("/")
async def crear_equipo(payload:Incidencia, request:Request):
    handdler = get_handdler(request)

    result = handdler.create(payload)

    return {'status': status.HTTP_201_CREATED, 'data': result.to_dict()}

@router.get("/{equipo_id}")
async def get_by_id(equipo_id: int, request:Request):
    handdler = get_handdler(request)

    result = handdler.get_by_id(equipo_id)

    if result == None:
        return {'status': status.HTTP_404_NOT_FOUND, 'data': 'Not in database'}
    
    return {'status': status.HTTP_200_OK, 'data': result.to_dict()}