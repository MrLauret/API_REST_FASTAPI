from api_rest_incidencia.models.tecnico import Tecnico
from sqlite3 import Connection

class HanddlerTecnicoDB:
    def __init__(self, conn:Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    def create(self, Tecnico:Tecnico):
        self.cursor.execute(
            'INSERT INTO tecnicos (nombre, especialidad, email) VALUES (?, ?, ?)', 
            (Tecnico.nombre, Tecnico.especialidad, Tecnico.email,)
        )

        self.conn.commit()

        Tecnico.id = cursor.lastrowid

        print(f'Técnico {Tecnico.nombre} creado')

        return Tecnico

    def get_by_id(self, id):
        self.cursor.execute('SELECT * FROM tecnicos WHERE id = ?', (id,))
        row = self.cursor.fetchone()

        if row == None:
            return None

        return Tecnico(**dict(row))

    def put(self, id, nombre, email, especialidad):
        try:
            self.cursor.execute('''
                UPDATE incidencias
                SET nombre = ?, email = ?, especialidad = ?
                WHERE id = ?;

            ''', (nombre, email, especialidad, id,)
            )

            if self.cursor.rowcount == 0:
                return False

            self.conn.commit()
            
            return True
        except Exception as e:
            print(f'Error en la base de datos {e}')
            return None