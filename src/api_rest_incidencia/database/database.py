import sqlite3
import pathlib
import logging

def get_db_connection(database_name):
    conn = sqlite3.connect(database_name)
    conn.row_factory = sqlite3.Row
    logging.info("Conexión con la base de datos creada")

    return conn

def db_migrate(cursor:sqlite3.Cursor):
    migrations_dir = pathlib.Path("src/api_rest_incidencia/database/migrations")

    for migration in sorted(migrations_dir.iterdir()):
        cursor.executescript(migration.read_text(encoding="utf-8"))
    
    logging.info("Migraciones en la base de datos correctas")