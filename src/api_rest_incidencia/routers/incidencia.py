from fastapi import APIRouter, Request, requests, status
from api_rest_incidencia.database import incidencias
from api_rest_incidencia.models.incidencia import Incidencia

router = APIRouter(
    prefix="/incidencias",
    tags=["incidencias"]
)

def get_handdler(request:Request) -> incidencias.HanddlerIncidenciaDB:
    return request.app.state.handdler_incidencia_db

@router.post("/")
async def crear_incidencia(payload:Incidencia, request:Request):
    handdler = get_handdler(request)

    result = handdler.create(payload)

    return {'status': status.HTTP_201_CREATED, 'data': result.to_dict()}

@router.get("/{incidencia_id}")
async def get_by_id(incidencia_id: int, request:Request):
    handdler = get_handdler(request)

    result = handdler.get_by_id(incidencia_id)

    if result == None:
        return {'status': status.HTTP_404_NOT_FOUND, 'data': 'Not in database'}
    
    return {'status': status.HTTP_200_OK, 'data': result.to_dict()}