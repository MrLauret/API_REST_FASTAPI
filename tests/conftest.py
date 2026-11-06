import pytest
from httpx import AsyncClient, ASGITransport
from src.api_rest_incidencia.main import app
from tests import mock

@pytest.fixture
async def client():
    app.state.handler_tecnico_db = mock.tecnicos.MockTecnicoDB()
    app.state.handler_equipo_db = mock.equipos.MockEquipoDB()
    app.state.handler_incidencia_db = mock.incidencias.MockincidenciaDB()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
