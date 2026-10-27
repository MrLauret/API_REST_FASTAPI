from fastapi import APIRouter, Request, requests, status
from api_rest_incidencia.database import equipo
from api_rest_incidencia.models.equipo import Equipo

router = APIRouter(
    prefix="/equipos",
    tags=["equipos"]
)

class PutRequest(BaseModel):
    nombre: str
    tipo: str
    ip: str
    ubicacion: str

def get_handdler(request:Request) -> equipo.HanddlerEquipoDB:
    return request.app.state.handdler_equipo_db

@router.post("/")
async def crear_equipo(payload:Incidencia, request:Request):
    handdler = get_handdler(request)

    result = handdler.create(payload)

    return Response(result.to_dict(), status.HTTP_201_CREATED)

@router.get("/{equipo_id}")
async def get_by_id(equipo_id: int, request:Request):
    handdler = get_handdler(request)

    result = handdler.get_by_id(equipo_id)

    if result == None:
        return Response(None, status.HTTP_404_NOT_FOUND)
    
    return Response(result.to_dict(), status.HTTP_200_OK)

@router.put("/{equipo_id}")
async def update(equipo_id: int, put_req:PutRequest, request:Request):
    handdler = get_handdler(request)
    result = handdler.put(equipo_id, **put_req)

    if not result:
        return Response(None, status.HTTP_404_NOT_FOUND)
    elif result == None:
        return Response(None, status.HTTP_304_NOT_MODIFIED)
    
    return Response(result.to_dict(), status.HTTP_200_OK)