from fastapi import APIRouter, Request, requests, status
from api_rest_incidencia.database import tecnicos
from api_rest_incidencia.models.tecnico import Tecnico

router = APIRouter(
    prefix="/tecnicos",
    tags=["tecnicos"]
)

def get_handdler(request:Request) -> tecnicos.HanddlerTecnicoDB:
    return request.app.state.handdler_tecnicos_db

@router.post("/")
async def crear_tecnico(payload:Incidencia, request:Request):
    handdler = get_handdler(request)

    result = handdler.create(payload)

    return {'status': status.HTTP_201_CREATED, 'data': result.to_dict()}

@router.get("/{tecnico_id}")
async def get_by_id(tecnico_id: int, request:Request):
    handdler = get_handdler(request)

    result = handdler.get_by_id(tecnico_id)

    if result == None:
        return {'status': status.HTTP_404_NOT_FOUND, 'data': 'Not in database'}
    
    return {'status': status.HTTP_200_OK, 'data': result.to_dict()}