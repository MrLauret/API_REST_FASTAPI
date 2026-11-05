from api_rest_incidencia.models import incidencia, errors
from psycopg.connection import Connection
from api_rest_incidencia.database import equipos, tecnicos
import datetime
import logging

class handlerIncidenciaDB:
    def __init__(self, conn:Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    def create(self, put_req):

        if equipos.handlerEquipoDB(self.conn).get_by_id(put_req.equipo_id) == None: 
            return errors.NoEquipo()

        self.cursor.execute(
            '''
            INSERT INTO incidencias
            (titulo, descripcion, prioridad, estado, equipo_id, tecnico_id, fecha_creacion, fecha_modificacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id''', 
            (
                put_req.titulo,
                put_req.descripcion,
                put_req.prioridad,
                put_req.estado,
                put_req.equipo_id,
                put_req.tecnico_id,
                self.fecha_actual(),
                self.fecha_actual(),
            )
        )

        generated_id = self.cursor.fetchone()["id"]
        self.conn.commit()

        logging.info(f'Incidencia {put_req.titulo} creada con id {generated_id}')

        return generated_id

    def get_by_id(self, id) -> incidencia.Incidencia | None:
        self.cursor.execute(
            'SELECT * FROM incidencias WHERE id = %s', (id,)
        )
        row = self.cursor.fetchone()

        if row == None:
            return None

        return incidencia.Incidencia(**row)
    
    def put(self, id, titulo:str, descripcion:str, prioridad:str, estado:str, equipo_id, tecnico_id) -> bool | errors.NoEquipo | errors.NoTecnico:
        try:
            if not equipos.handlerEquipoDB(self.conn).get_by_id(equipo_id): 
                return errors.NoEquipo
            
            if type(tecnico_id) != None and not tecnicos.handlerTecnicoDB(self.conn).get_by_id(tecnico_id):
                return errors.NoTecnico

            self.cursor.execute('''
                UPDATE incidencias
                SET titulo = %s, descripcion = %s, prioridad = %s, estado = %s, equipo_id = %s, tecnico_id = %s, fecha_modificacion = %s
                WHERE id = %s;

            ''', (titulo, descripcion, prioridad, estado, equipo_id, tecnico_id, self.fecha_actual(), id,)
            )

            if self.cursor.rowcount == 0:
                self.cursor.rollback()
                return False

            self.conn.commit()
            logging.info(f"Incidendia con id: {id} actualizada")
            
            return True
        except Exception as e:
            logging.error(f'Error en la base de datos {e} el {self.fecha_actual()}')
            return None
    
    def delete(self, id):
        try:
            self.cursor.execute('''
                DELETE FROM incidencias WHERE id = %s;
            ''', (id,))

            if self.cursor.rowcount == 0:
                self.cursor.rollback()
                return False
            
            self.conn.commit()
            logging.info(f"Incidencia con id: {id} borrada")

            return True
        except Exception as e:
            logging.error(f'Error en la base de datos {e} el {self.fecha_actual()}')
            return None
    
    def cerrar(self, id):
        try:
            self.cursor.execute('''
                UPDATE incidencias
                SET fecha_modificacion = %s, estado = 'cerrada'
                WHERE id = %s;
            ''', (self.fecha_actual(), id,))

            if self.cursor.rowcount == 0:
                self.cursor.rollback()
                return False
            
            self.conn.commit()
            logging.info(f"Incidencia con id: {id} se ha cerrado")

            return True
        except Exception as e:
            logging.error(f'Error en la base de datos {e} el {self.fecha_actual()}')
            return None
    
    def asignar_tecnico(self, id, id_tecnico) -> bool | errors.NoTecnico:
        try:
            if not tecnicos.handlerTecnicoDB(self.conn).get_by_id(id_tecnico):
                return errors.NoTecnico()

            self.cursor.execute('''
                UPDATE incidencias
                SET fecha_modificacion = %s, tecnico_id = %s
                WHERE id = %s;
            ''', (self.fecha_actual(), id_tecnico, id,))

            if self.cursor.rowcount == 0:
                self.cursor.rollback()
                return False
            
            self.cursor.commit()

        except Exception as e:
            logging.error(f'Error en la base de datos {e} el {self.fecha_actual()}')
            return None
    
    def lista(self):
        self.cursor.execute('''
            SELECT * FROM incidencias;
        ''')

        return self.cursor.fetchall()
    
    @staticmethod
    def fecha_actual():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')