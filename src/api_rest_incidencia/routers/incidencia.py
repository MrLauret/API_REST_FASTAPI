from fastapi import APIRouter, Request, status, Response
from fastapi.responses import JSONResponse
from api_rest_incidencia.database import incidencias
from api_rest_incidencia.models.errors import *
from api_rest_incidencia.models.incidencia import Incidencia, Prioridad, Estado
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/api/incidencias",
    tags=["incidencias"]
)

class AsignarTecnico(BaseModel):
    tecnico_id: Optional[int]

class PutRequest(BaseModel):
    titulo: str
    descripcion: Optional[str]
    prioridad: str
    estado: str
    equipo_id: int
    tecnico_id: Optional[int]

def get_handler(request:Request) -> incidencias.HanddlerIncidenciaDB:
    return request.app.state.handdler_incidencia_db


@router.post("/")
async def crear_incidencia(payload:PutRequest, request:Request):
    handdler = get_handler(request)

    result = handdler.create(**payload.dict())

    if hasattr(result, "to_dict") and callable(result.to_dict):
        return JSONResponse(result.to_dict(), status_code=status.HTTP_201_CREATED)
    return JSONResponse(content={"error": "Result object does not implement to_dict()"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/{incidencia_id}/")
async def get_by_id(incidencia_id: int, request:Request):
    handdler = get_handler(request)

    result = handdler.get_by_id(incidencia_id)

    if result is None:
        return JSONResponse(content=None, status_code=status.HTTP_404_NOT_FOUND)
    
    if hasattr(result, "to_dict") and callable(result.to_dict):
        return JSONResponse(content=result.to_dict(), status_code=status.HTTP_200_OK)
    return JSONResponse(content={"error": "Result object does not implement to_dict()"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put("/{incidencia_id}/")
async def update(incidencia_id: int, put_req:PutRequest, request:Request):

    if not Estado.check_valido(put_req.estado):
        return JSONResponse(content={"error": "Estado debe ser 'Abierta', 'En proceso', 'Cerrada'"}, status_code=status.HTTP_400_BAD_REQUEST)

    elif not Prioridad.check_valido(put_req.prioridad):
        return JSONResponse(content={"error": "Prioridad debe ser 'Baja', 'Media', 'Alta', 'Critica'"}, status_code=status.HTTP_400_BAD_REQUEST)

    handdler = get_handdler(request)
    result = handdler.put(incidencia_id, **put_req.dict())

    if isinstance(result, NoEquipo):
        return JSONResponse(content={"Error": "Ningun equipo fue encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
    
    if isinstance(result, NoTecnico):
        return JSONResponse(content={"Error": "Ningun tecnico fue encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

    if result is None:
        return JSONResponse(content=None, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=result.to_dict(), status_code=status.HTTP_200_OK)

@router.patch("/{incidencia_id}/cerrar/")
async def cerrar_incidencia(incidencia_id: int, request:Request):
    handdler = get_handler(request)

    result = handdler.cerrar(incidencia_id)

    if result is None:
        return JSONResponse(content=None, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=result.to_dict(), status_code=status.HTTP_200_OK)

@router.patch("/{incidencia_id}/asignar_tecnico/")
async def asignar_tecnico(incidencia_id: int, payload: AsignarTecnico, request:Request):
    handdler = get_handler(request)

    result = handdler.asignar_tecnico(incidencia_id, payload.tecnico_id)

    if isinstance(result, NoTecnico):
        return JSONResponse(content={"Error": "Ningun tecnico fue encontrado"}, status_code=status.HTTP_304_NOT_MODIFIED)
    if result is None:
        return JSONResponse(content=None, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=result.to_dict(), status_code=status.HTTP_200_OK)