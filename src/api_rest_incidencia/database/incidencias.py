from api_rest_incidencia.models.incidencia import Incidencia
from sqlite3 import Connection

class HanddlerIncidenciaDB:
    def __init__(self, conn:Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    def create(self, incidencia:Incidencia):
        self.cursor.execute(
            'INSERT INTO incidencias (titulo, descripcion, prioridad, estado, equipo_id, tecnico_id, fecha_creacion, fecha_modificacion) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
            (incidencia.titulo, incidencia.descripcion, incidencia.prioridad, incidencia.estado, incidencia.equipo_id, incidencia.tecnico_id, incidencia.fecha_creacion, incidencia.fecha_modificacion,)
        )

        self.conn.commit()

        Tecnico.id = cursor.lastrowid

        print(f'Incidencia {incidencia.nombre} creado')

        return incidencia

    def get_by_id(self, id):
        self.cursor.execute('SELECT * FROM incidencias WHERE id = ?', (id,))
        row = self.cursor.fetchone()

        if row == None:
            return None

        return Incidencia(**dict(row))