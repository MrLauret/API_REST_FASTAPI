from fastapi import APIRouter, Request, requests, status
from api_rest_incidencia.database import tecnicos
from api_rest_incidencia.models.tecnico import Tecnico

router = APIRouter(
    prefix="/tecnicos",
    tags=["tecnicos"]
)

class PutRequest(BaseModel):
    nombre: str
    email: str
    especialidad: str

def get_handdler(request:Request) -> tecnicos.HanddlerTecnicoDB:
    return request.app.state.handdler_tecnicos_db

@router.post("/")
async def crear_tecnico(payload:Incidencia, request:Request):
    handdler = get_handdler(request)

    result = handdler.create(payload)

    return Response(result.to_dict(), status.HTTP_201_CREATED)

@router.get("/{tecnico_id}")
async def get_by_id(tecnico_id: int, request:Request):
    handdler = get_handdler(request)

    result = handdler.get_by_id(tecnico_id)

    if result == None:
        return Response(None, status.HTTP_404_NOT_FOUND)
    
    return Response(result.to_dict(), status.HTTP_200_OK)

@router.put("/{tecnico_id}")
async def update(tecnico_id: int, put_req:PutRequest, request:Request):
    handdler = get_handdler(request)
    result = handdler.put(tecnico_id, **put_req)

    if not result:
        return Response(None, status.HTTP_404_NOT_FOUND)
    elif result == None:
        return Response(None, status.HTTP_304_NOT_MODIFIED)
    
    return Response(result.to_dict(), status.HTTP_200_OK)