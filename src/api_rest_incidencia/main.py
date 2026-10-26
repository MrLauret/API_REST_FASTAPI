import os
from dotenv import load_dotenv
from api_rest_incidencia.database.database import get_db_connection, db_migrate

def main() -> None:
    load_dotenv()
    database_name = os.getenv('db_name')

    conn = get_db_connection(database_name)
    cursor = conn.cursor()
    db_migrate(cursor)

if __name__ == "__main__":
    main()