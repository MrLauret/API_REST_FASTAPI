from api_rest_incidencia.models.incidencia import Incidencia
from sqlite3 import Connection
import datetime
import logging

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

        logging.info(f'Incidencia {incidencia.nombre} creada')

        return incidencia

    def get_by_id(self, id):
        self.cursor.execute('SELECT * FROM incidencias WHERE id = ?', (id,))
        row = self.cursor.fetchone()

        if row == None:
            return None

        return Incidencia(**dict(row))
    
    def put(self, id, titulo, descripcion, prioridad, estado, equipo_id, tecnico_id):
        try:
            fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute('''
                UPDATE incidencias
                SET titulo = ?, descripcion = ?, prioridad = ?, estado = ?, equipo_id = ?, tecnico_id = ?, fecha_modificacion = ?
                WHERE id = ?;

            ''', (titulo, descripcion, prioridad, estado, equipo_id, tecnico_id, fecha_actual, id,)
            )

            if self.cursor.rowcount == 0:
                return False

            self.conn.commit()
            
            return True
        except Exception as e:
            logging.error(f'Error en la base de datos {e}')
            return None
    
    def delete(self, id):
        try:
            self.cursor.execute('''
                DELETE FROM incidencias WHERE id = ?;
            ''', (id,))

            if self.cursor.rowcount == 0:
                return False
            
            self.conn.commit()

            return True
        except Exception as e:
            logging.error(f'Error en la base de datos {e}')
            return None
    
    def cerrar(self, id):
        try:
            fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute('''
                UPDATE incidencias
                SET fecha_modificacion = ?, estado = 'cerrada'
                WHERE id = ?;
            ''', (fecha_actual, id,))

            if self.cursor.rowcount == 0:
                return False
            
            self.conn.commit()

            return True
        except Exception as e:
            logging.error(f'Error en la base de datos {e}')
            return None