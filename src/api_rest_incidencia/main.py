import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api_rest_incidencia.database import database, equipos, incidencias, tecnicos
from api_rest_incidencia.routers import equipo, incidencia, tecnico

app = FastAPI()

def main() -> None:
    load_dotenv()
    database_name = os.getenv('db_name')

    conn = database.get_db_connection(database_name)
    cursor = conn.cursor()
    database.db_migrate(cursor)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],

    )

    HanddlerIncidenciaDB = incidencias.HanddlerIncidenciaDB(conn)
    HanddlerEquipoDB = equipos.HanddlerEquipoDB(conn)
    HanddlerTecnicoDB = tecnicos.HanddlerTecnicoDB

    app.state.handdler_incidencia_db = HanddlerIncidenciaDB
    app.state.handdler_equipo_db = HanddlerEquipoDB
    app.state.handdler_tecnico_db = HanddlerTecnicoDB

    app.include_router(incidencia.router)
    app.include_router(tecnico.router)
    app.include_router(equipo.router)

if __name__ == "__main__":
    main()