from fastapi import APIRouter, Request, Response, status
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
    
@router.post("/")
async def crear_tecnico(payload: PutRequest, request: Request):
    handdler = get_handler(request)

    result = handdler.create(payload)

    if result is None:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return Response(result.to_dict(), status.HTTP_201_CREATED)

@router.get("/{tecnico_id}/")
async def get_by_id(tecnico_id: int, request: Request):
    handdler = get_handler(request)

    result = handdler.get_by_id(tecnico_id)
    if result is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    if hasattr(result, "to_dict") and callable(result.to_dict):
        return Response(result.to_dict(), status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put("/{tecnico_id}/")
async def update(tecnico_id: int, put_req: PutRequest, request: Request):

    handdler = get_handler(request)
    result = handdler.put(tecnico_id, **put_req.dict())

    if not result:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    elif result is None:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)
    
    if hasattr(result, "to_dict") and callable(result.to_dict):
        return Response(result.to_dict(), status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if hasattr(result, "to_dict") and callable(result.to_dict):
        return Response(result.to_dict(), status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(result.to_dict(), status.HTTP_200_OK)