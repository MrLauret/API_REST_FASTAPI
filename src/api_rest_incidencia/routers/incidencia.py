from fastapi import APIRouter, Request, requests, status, Response
from api_rest_incidencia.database import incidencias
from api_rest_incidencia.models.errors import *
from api_rest_incidencia.models.incidencia import Incidencia, Prioridad, Estado
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/incidencias",
    tags=["incidencias"]
)

class AsignarTecnico(BaseModel):
    tecnico_id: int | None

class PutRequest(BaseModel):
    titulo: str
    descripcion: str | None
    prioridad: str
    estado: str
    equipo_id: int
    tecnico_id: int | None

def get_handdler(request:Request) -> incidencias.HanddlerIncidenciaDB:
    return request.app.state.handdler_incidencia_db


@router.post("/")
async def crear_incidencia(payload:PutRequest, request:Request):
    handdler = get_handdler(request)

    result = handdler.create(**payload)

    return Response(result.to_dict(), status.HTTP_201_CREATED)

@router.get("/{incidencia_id}/")
async def get_by_id(incidencia_id: int, request:Request):
    handdler = get_handdler(request)

    result = handdler.get_by_id(incidencia_id)

    if result == None:
        return Response(None, status.HTTP_404_NOT_FOUND)
    
    return Response(result.to_dict(), status.HTTP_200_OK)

@router.put("/{incidencia_id}/")
async def update(incidencia_id: int, put_req:PutRequest, request:Request):

    if not Estado.check_valido(put_req.estado):
        return Response("Estado debe ser 'Abierta', 'En proceso', 'Cerrada'", status.HTTP_400_BAD_REQUEST)

    elif not Prioridad.check_valido(put_req.prioridad):
        return Response("Prioridad debe ser 'Baja', 'Media', 'Alta', 'Critica'", status.HTTP_400_BAD_REQUEST)

    handdler = get_handdler(request)
    result = handdler.put(incidencia_id, **put_req)

    if type(result) == NoEquipo():
        return Response({"Error": "Ningun equipo fue encontrado"}, status_code=status.HTTP_304_NOT_MODIFIED)
    
    if type(result) == NoTecnico():
        return Response({"Error": "Ningun tecnico fue encontrado"}, status_code=status.HTTP_304_NOT_MODIFIED)

    if not result:
        return Response(None, status.HTTP_404_NOT_FOUND)
    elif result == None:
        return Response(None, status.HTTP_304_NOT_MODIFIED)
    
    return Response(result.to_dict(), status.HTTP_200_OK)

@router.patch("/{incidencia_id}/cerrar/")
async def cerrar_incidencia(incidencia_id: int, request:Request):
    handdler = get_handdler(request)

    result = handdler.cerrar(incidencia_id)

    if not result:
        return Response(None, status.HTTP_404_NOT_FOUND)
    elif result == None:
        return Response(None, status.HTTP_304_NOT_MODIFIED)
    
    return Response(result.to_dict(), status.HTTP_200_OK)

@router.patch("/{incidencia_id}/asignar_tecnico/")
async def asignar_tecnico(incidencia_id, payload:AsignarTecnico, request:Request):
    handdler = get_handdler(request)

    pass