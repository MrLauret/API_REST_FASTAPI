from api_rest_incidencia.models.equipo import Equipo
from sqlite3 import Connection

class HanddlerEquipoDB:
    def __init__(self, conn:Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    def create(self, Equipo:Equipo):
        self.cursor.execute(
            'INSERT INTO equipos (nombre, tipo, ip, ubicacion) VALUES (?, ?, ?, ?)', 
            (Equipo.nombre, Equipo.tipo, Equipo.ip, Equipo.ubicacion,)
        )

        self.conn.commit()

        Equipo.id = cursor.lastrowid

        print(f'Equipo {Equipo.nombre} creado')

        return Equipo

    def get_by_id(self, id):
        self.cursor.execute('SELECT * FROM equipos WHERE id = ?', (id,))
        row = self.cursor.fetchone()

        if row == None:
            return None

        return Equipo(**dict(row))

    def put(self, id, nombre, tipo, ip, ubicacion):
        try:
            self.cursor.execute('''
                UPDATE incidencias
                SET nombre = ?, tipo = ?, ip = ?, ubicacion = ?
                WHERE id = ?;

            ''', (nombre, tipo, ip, ubicacion, id,)
            )

            if self.cursor.rowcount == 0:
                return False

            self.conn.commit()
            
            return True
        except Exception as e:
            print(f'Error en la base de datos {e}')
            return None