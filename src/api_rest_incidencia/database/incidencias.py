from api_rest_incidencia.models.incidencia import Incidencia
from psycopg.connection import Connection
import datetime
import logging

class HanddlerIncidenciaDB:
    def __init__(self, conn:Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    def create(self, incidencia:Incidencia) -> Incidencia:

        self.cursor.execute(
            '''
            INSERT INTO incidencias
            (titulo, descripcion, prioridad, estado, equipo_id, tecnico_id, fecha_creacion, fecha_modificacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id''', 
            (
                incidencia.titulo,
                incidencia.descripcion,
                incidencia.prioridad,
                incidencia.estado,
                incidencia.equipo_id,
                incidencia.tecnico_id,
                incidencia.fecha_creacion,
                incidencia.fecha_modificacion,
            )
        )

        generated_id = self.cursor.fetchone()[0]
        self.conn.commit()

        incidencia.id = generated_id

        logging.info(f'Incidencia {incidencia.nombre} creada con id {generated_id}')

        return incidencia

    def get_by_id(self, id) -> Incidencia | None:
        self.cursor.execute(
            'SELECT * FROM incidencias WHERE id = %s', (id,)
        )
        row = self.cursor.fetchone()

        if row == None:
            return None

        return Incidencia(**row)
    
    def put(self, id, titulo:str, descripcion:str, prioridad:str, estado:str, equipo_id, tecnico_id) -> bool:
        try:
            fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute('''
                UPDATE incidencias
                SET titulo = %s, descripcion = %s, prioridad = %s, estado = %s, equipo_id = %s, tecnico_id = %s, fecha_modificacion = %s
                WHERE id = %s;

            ''', (titulo, descripcion, prioridad, estado, equipo_id, tecnico_id, fecha_actual, id,)
            )

            if self.cursor.rowcount == 0:
                return False

            self.conn.commit()
            logging.info(f"Incidendia con id: {id} actualizada")
            
            return True
        except Exception as e:
            logging.error(f'Error en la base de datos {e}')
            return None
    
    def delete(self, id):
        try:
            self.cursor.execute('''
                DELETE FROM incidencias WHERE id = %s;
            ''', (id,))

            if self.cursor.rowcount == 0:
                return False
            
            self.conn.commit()
            logging.info(f"Incidencia con id: {id} borrada")

            return True
        except Exception as e:
            logging.error(f'Error en la base de datos {e}')
            return None
    
    def cerrar(self, id):
        try:
            fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute('''
                UPDATE incidencias
                SET fecha_modificacion = %s, estado = 'cerrada'
                WHERE id = %s;
            ''', (fecha_actual, id,))

            if self.cursor.rowcount == 0:
                return False
            
            self.conn.commit()
            logging.info(f"Incidencia con id: {id} se ha cerrado")

            return True
        except Exception as e:
            logging.error(f'Error en la base de datos {e}')
            return None