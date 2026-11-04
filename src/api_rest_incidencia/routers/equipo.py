from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from api_rest_incidencia.database import equipos
from api_rest_incidencia.models.equipo import Equipo
from api_rest_incidencia.database.equipos import HanddlerEquipoDB
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/equipos",
    tags=["equipos"]
)

class PutRequest(BaseModel):
    nombre: str
    tipo: str
    ip: str
    ubicacion: str



def get_handler(request: Request) -> HanddlerEquipoDB:
    return request.app.state.handdler_equipo_db

@router.post("/")
async def crear_equipo(payload:PutRequest, request:Request):
    handdler = get_handler(request)

    result = handdler.create(payload)

    if result is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"id": result}, status.HTTP_201_CREATED)

@router.get("/{equipo_id}/")
async def get_by_id(equipo_id: int, request:Request):
    handdler = get_handler(request)

    result = handdler.get_by_id(equipo_id)

    if result == None:
        return Response(None, status.HTTP_404_NOT_FOUND)
    
    return Response(result.dict(), status.HTTP_200_OK)

@router.put("/{equipo_id}/")
async def update_equipo(equipo_id: int, payload: PutRequest, request: Request):
    handdler = get_handler(request)
    result = handdler.put(equipo_id, **payload.dict())

    if result is None:
        return Response(None, status.HTTP_404_NOT_FOUND)
    
    return Response(result.dict(), status.HTTP_200_OK)