from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from api_rest_incidencia.database import equipos
from api_rest_incidencia.models.equipo import Equipo
from api_rest_incidencia.database.equipos import handlerEquipoDB
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


def get_handler(request: Request) -> handlerEquipoDB:
    return request.app.state.handler_equipo_db

@router.get("/")
async def lista_equipo(request: Request):
    handler = get_handler(request)

    return handler.lista()

@router.post("/")
async def crear_equipo(payload:PutRequest, request:Request):
    handler = get_handler(request)
    result = handler.create(payload)
    
    return JSONResponse({"id": result}, status.HTTP_201_CREATED)

@router.get("/{equipo_id}/")
async def get_by_id(equipo_id: int, request:Request):
    handler = get_handler(request)
    result = handler.get_by_id(equipo_id)

    if not result:
        return JSONResponse({"Error": "Ningun equipo fue encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
    if result == None:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return JSONResponse(result, status.HTTP_200_OK)

@router.put("/{equipo_id}/")
async def update_equipo(equipo_id: int, payload: PutRequest, request: Request):
    handler = get_handler(request)
    result = handler.put(equipo_id, **payload.model_dump())

    if not result:
        return JSONResponse({"Error": "Ningun equipo fue encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
    if result == None:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return JSONResponse({"Mensaje": "Editado con exito"}, status_code=status.HTTP_200_OK)

@router.delete("/{equipo_id}/")
async def borrar_equipo(equipo_id: int, request: Request):
    handler = get_handler(request)
    result = handler.delete(equipo_id)

    if result is None:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if not result:
        return JSONResponse({"Error": "Ningun equipo fue encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse({"Mensaje": f"Equipo {equipo_id} borrado"}, status_code=status.HTTP_200_OK)