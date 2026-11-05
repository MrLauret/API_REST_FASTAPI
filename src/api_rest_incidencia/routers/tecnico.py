from fastapi import APIRouter, Request, Response, status, HTTPException
from fastapi.responses import JSONResponse
from api_rest_incidencia.database import tecnicos
from api_rest_incidencia.models.tecnico import Tecnico
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/tecnicos",
    tags=["tecnicos"]
)

class PutRequest(BaseModel):
    nombre: str
    email: str
    especialidad: str

def get_handler(request:Request) -> incidencias.handlerIncidenciaDB:
    return request.app.state.handler_tecnico_db

@router.get("/")
async def lista_tecnico(request: Request):
    handler = get_handler(request)

    return handler.lista()

@router.post("/")
async def crear_tecnico(payload: PutRequest, request: Request):
    handler = get_handler(request)
    result = handler.create(payload)

    if result is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"id": result}, status.HTTP_201_CREATED)

@router.get("/{tecnico_id}/")
async def get_by_id(tecnico_id: int, request: Request):
    handler = get_handler(request)

    result = handler.get_by_id(tecnico_id)
    if result is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(result, status.HTTP_200_OK)

@router.put("/{tecnico_id}/")
async def update(tecnico_id: int, put_req: PutRequest, request: Request):

    handler = get_handler(request)
    result = handler.put(tecnico_id, **put_req.dict())

    if not result:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif result is None:
        return JSONResponse({"Error": "Ningun tecnico fue encontrado"}, status_code=status.HTTP_304_NOT_MODIFIED)
    
    return JSONResponse({"Mensaje": "Editado con exito"}, status_code=status.HTTP_200_OK)