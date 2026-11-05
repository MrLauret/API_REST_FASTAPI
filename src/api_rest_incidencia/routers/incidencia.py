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
    descripcion: str | None
    prioridad: str
    estado: str
    equipo_id: int
    tecnico_id: int | None

def get_handler(request:Request) -> incidencias.handlerIncidenciaDB:
    return request.app.state.handler_incidencia_db

@router.get("/")
async def lista_incidencia(request: Request):
    handler = get_handler(request)
    return handler.lista()

@router.post("/")
async def crear_incidencia(payload:PutRequest, request:Request):
    handler = get_handler(request)
    result = handler.create(payload)

    if isinstance(result, NoEquipo):
        return JSONResponse(content={"Error": "Ningun equipo fue encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse({"id": result}, status_code=status.HTTP_201_CREATED)

@router.get("/{incidencia_id}/")
async def get_by_id(incidencia_id: int, request:Request):
    handler = get_handler(request)
    result = handler.get_by_id(incidencia_id)

    if not result:
        return JSONResponse({"Error": "Ninguna incidecia fue encontrada"}, status_code=status.HTTP_404_NOT_FOUND)
    
    if hasattr(result, "to_dict") and callable(result.to_dict):
        return JSONResponse(content=result.to_dict(), status_code=status.HTTP_200_OK)
    return JSONResponse(content={"error": "Result object does not implement to_dict()"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put("/{incidencia_id}/")
async def update(incidencia_id: int, put_req:PutRequest, request:Request):

    if not Estado.check_valido(put_req.estado):
        return JSONResponse(content={"error": "Estado debe ser 'Abierta', 'En proceso', 'Cerrada'"}, status_code=status.HTTP_400_BAD_REQUEST)

    elif not Prioridad.check_valido(put_req.prioridad):
        return JSONResponse(content={"error": "Prioridad debe ser 'Baja', 'Media', 'Alta', 'Critica'"}, status_code=status.HTTP_400_BAD_REQUEST)

    handler = get_handler(request)
    result = handler.put(incidencia_id, **put_req.dict())

    if isinstance(result, NoEquipo):
        return JSONResponse(content={"Error": "Ningun equipo fue encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
    
    if isinstance(result, NoTecnico):
        return JSONResponse(content={"Error": "Ningun tecnico fue encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

    if not result:
        return JSONResponse({"Error": "Ninguna incidecia fue encontrada"}, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse({"Mensaje": "Editado con exito"}, status_code=status.HTTP_200_OK)

@router.patch("/{incidencia_id}/cerrar/")
async def cerrar_incidencia(incidencia_id: int, request:Request):
    handler = get_handler(request)
    result = handler.cerrar(incidencia_id)

    if not result:
        return JSONResponse({"Error": "Ninguna incidecia fue encontrada"}, status_code=status.HTTP_404_NOT_FOUND)
    if result == None:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return JSONResponse({"Mensaje": "Incidencia cerrada correctamente"}, status_code=status.HTTP_200_OK)

@router.patch("/{incidencia_id}/asignar_tecnico/")
async def asignar_tecnico(incidencia_id: int, payload: AsignarTecnico, request:Request):
    handler = get_handler(request)
    result = handler.asignar_tecnico(incidencia_id, payload.tecnico_id)

    if isinstance(result, NoTecnico):
        return JSONResponse(content={"Error": "Ningun tecnico fue encontrado"}, status_code=status.HTTP_304_NOT_MODIFIED)
    if not result:
        return JSONResponse({"Error": "Ninguna incidecia fue encontrada"}, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)

@router.delete("/{incidencia_id}/")
async def borrar_incidencia(incidencia_id: int, request: Request):
    handler = get_handler(request)
    result = handler.delete(incidencia_id)

    if result is None:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if not result:
        return JSONResponse({"Error": "Ninguna incidecia fue encontrada"}, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse({"Mensaje": f"Incidencia {incidencia_id} borrada"}, status_code=status.HTTP_200_OK)