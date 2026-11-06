import pytest
from httpx import AsyncClient, ASGITransport

async def test_get_incidencias_list(client: AsyncClient):
    response = await client.get("/api/incidencias/")
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1,
        "titulo": "pc roto",
        "descripcion": "no va",
        "prioridad": "baja",
        "estado": "En proceso",
        "equipo_id": "1",
        "tecnico_id": "1",
        "fecha_creación": "hoy",
        "fecha_modificacion": "hoy"
    }]

@pytest.mark.asyncio
async def test_get_incidencia_by_id(client: AsyncClient):
    response = await client.get("/api/incidencias/1/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "titulo": "pc roto",
        "descripcion": "no va",
        "prioridad": "baja",
        "estado": "En proceso",
        "equipo_id": "1",
        "tecnico_id": "1",
        "fecha_creación": "hoy",
        "fecha_modificacion": "hoy"
    }

@pytest.mark.asyncio
async def test_create_incidencia(client: AsyncClient):
    response = await client.post(
        "/api/incidencias/",
        json={
            "titulo": "pc roto",
            "descripcion": "no va",
            "prioridad": "baja",
            "estado": "En proceso",
            "equipo_id": "1",
            "tecnico_id": "1",
        },
    )
    assert response.status_code == 201
    assert response.json() == {"id": 2}

@pytest.mark.asyncio
async def test_update_incidencia(client: AsyncClient):
    response = await client.put(
        "/api/incidencias/1/",
        json={
            "titulo": "pc roto",
            "descripcion": "no va",
            "prioridad": "critica",
            "estado": "En proceso",
            "equipo_id": "1",
            "tecnico_id": "1",
            "fecha_creacion": "hoy",
            "fecha_modificacion": "ahora"
        },
    )
    assert response.status_code == 200
    assert response.json() == {"Mensaje": "Editado con exito"}

@pytest.mark.asyncio
async def test_delete_incidencia(client: AsyncClient):
    response = await client.delete("/api/incidencias/1/")
    assert response.status_code == 200
    assert response.json() == {"Mensaje": "Incidencia 1 borrada"}

@pytest.mark.asyncio
async def test_asignar_tecnico_incidencia(client: AsyncClient):
    response = await client.patch(
        "/api/incidencias/1/asignar_tecnico/",
        json={
            "tecnico_id": 1
        }
    )

    assert response.status_code == 200
    assert response.json() == {"Mensaje": "Tecnico asignado a incidencia"}

@pytest.mark.asyncio
async def test_cerrar_incidencia(client: AsyncClient):
    response = await client.patch(
        "/api/incidencias/1/cerrar/",
        json={
            "tecnico_id": 1
        }
    )

    assert response.status_code == 200
    assert response.json() == {"Mensaje": "Incidencia cerrada correctamente"}