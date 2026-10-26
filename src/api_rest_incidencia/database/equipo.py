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