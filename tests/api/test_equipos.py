import pytest
from httpx import AsyncClient, ASGITransport

async def test_get_equipos_list(client: AsyncClient):
    response = await client.get("/api/equipos/")
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1,
        "nombre": "servidor",
        "tipo": "hardware",
        "ip": "111.23.41.6",
        "ubicacion": "Madrid"
    }]

@pytest.mark.asyncio
async def test_get_equipo_by_id(client: AsyncClient):
    response = await client.get("/api/equipos/1/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "nombre": "servidor",
        "tipo": "hardware",
        "ip": "111.23.41.6",
        "ubicacion": "Madrid"
    }

@pytest.mark.asyncio
async def test_create_tecnico(client: AsyncClient):
    response = await client.post(
        "/api/equipos/",
        json={
            "nombre": "pc roto o algo",
            "tipo": "hardware",
            "ip": "111.23.41.6",
            "ubicacion": "Barcelona"
        },
    )
    assert response.status_code == 201
    assert response.json() == {"id": 2}

@pytest.mark.asyncio
async def test_update_tecnico(client: AsyncClient):
    response = await client.put(
        "/api/equipos/1/",
        json={
            "nombre": "servidor",
            "tipo": "software",
            "ip": "111.23.41.6",
            "ubicacion": "Madrid"
        },
    )
    assert response.status_code == 200
    assert response.json() == {"Mensaje": "Editado con exito"}

@pytest.mark.asyncio
async def test_delete_tecnico(client: AsyncClient):
    response = await client.delete("/api/equipos/1/")
    assert response.status_code == 200
    assert response.json() == {"Mensaje": "Equipo 1 borrado"}