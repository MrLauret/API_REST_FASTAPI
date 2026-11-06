import pytest
from httpx import AsyncClient, ASGITransport

@pytest.mark.asyncio
async def test_get_tecnicos_list(client: AsyncClient):
    response = await client.get("/api/tecnicos/")
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1,
        "nombre": "Ana García",
        "email": "ana@example.com",
        "especialidad": "Sistemas",
    }]


@pytest.mark.asyncio
async def test_get_tecnico_by_id(client: AsyncClient):
    response = await client.get("/api/tecnicos/1/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "nombre": "Ana García",
        "email": "ana@example.com",
        "especialidad": "Sistemas",
    }


@pytest.mark.asyncio
async def test_create_tecnico(client: AsyncClient):
    response = await client.post(
        "/api/tecnicos/",
        json={
            "nombre": "Luis Pérez",
            "email": "luis@example.com",
            "especialidad": "Redes",
        },
    )
    assert response.status_code == 201
    assert response.json() == {"id": 2}


@pytest.mark.asyncio
async def test_update_tecnico(client: AsyncClient):
    response = await client.put(
        "/api/tecnicos/1/",
        json={
            "nombre": "Ana Gómez",
            "email": "ana.gomez@example.com",
            "especialidad": "Infraestructura",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"Mensaje": "Editado con exito"}


@pytest.mark.asyncio
async def test_delete_tecnico(client: AsyncClient):
    response = await client.delete("/api/tecnicos/1/")
    assert response.status_code == 200
    assert response.json() == {"Mensaje": "Tecnico 1 borrado"}