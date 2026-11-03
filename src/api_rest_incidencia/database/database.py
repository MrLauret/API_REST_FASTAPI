import psycopg
from psycopg.rows import dict_row
import pathlib
import logging

def get_db_connection(host, db_name, db_user, db_password, db_port):
    conn = psycopg.connect(
        host=host,
        dbname=db_name,
        user=db_user,
        password=db_password,
        port=db_port,
        row_factory=dict_row,
    )

    logging.info("Conexión con la base de datos creada")

    return conn

def db_migrate(cursor:psycopg.cursor.Cursor):
    migrations_dir = pathlib.Path("src/api_rest_incidencia/database/migrations")

    for migration in sorted(migrations_dir.iterdir()):
        cursor.execute(migration.read_text(encoding="utf-8"))
    
    logging.info("Migraciones en la base de datos correctas")