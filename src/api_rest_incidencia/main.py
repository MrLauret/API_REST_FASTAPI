import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv
from api_rest_incidencia import database, routers
from config import log_config
import json

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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    missing_fields = []

    for error in exc.errors():
        missing_fields = error.copy()
    
    if missing_fields:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Missing Required Fields",
                "explanation": "La request no contiene los fields necesarios",
                "missing_fields": missing_fields
            }
        )


    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "details": missing_fields
        }
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.incidencia.router)
app.include_router(routers.tecnico.router)
app.include_router(routers.equipo.router)
