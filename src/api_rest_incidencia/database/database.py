import sqlite3
import pathlib

def get_db_connection(database_name):
    conn = sqlite3.connect(database_name)
    conn.row_factory = sqlite3.Row

    return conn

def db_migrate(cursor:sqlite3.Cursor):
    migrations_dir = pathlib.Path("src/api_rest_incidencia/database/migrations")

    for migration in sorted(migrations_dir.iterdir()):
        cursor.executescript(migration.read_text(encoding="utf-8"))