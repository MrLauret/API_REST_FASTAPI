import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api_rest_incidencia import database, routers
from config import log_config

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    envs = {
        "host": os.getenv('host'),
        "db_name": os.getenv('db_name'),
        "db_password": os.getenv('db_password'),
        "db_port": os.getenv('db_port'),
        "db_user": os.getenv('db_user')
    }

    conn = database.get_db_connection(**envs)
    cursor = conn.cursor()
    database.db_migrate(cursor)
    
    app.state.handdler_incidencia_db = database.incidencias.HanddlerIncidenciaDB(conn)
    app.state.handdler_equipo_db = database.equipos.HanddlerEquipoDB(conn)
    app.state.handdler_tecnico_db = database.tecnicos.HanddlerTecnicoDB(conn)
    
    yield
    
    conn.close()

logging.config.dictConfig(log_config.LOGGING_CONFIG)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.incidencia.router)
app.include_router(routers.tecnico.router)
app.include_router(routers.equipo.router)
