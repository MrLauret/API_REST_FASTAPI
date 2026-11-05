from api_rest_incidencia.models.equipo import Equipo
from sqlite3 import Connection
import logging

class handlerEquipoDB:
    def __init__(self, conn:Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    def create(self, put_req):
        self.cursor.execute(
            'INSERT INTO equipos (nombre, tipo, ip, ubicacion) VALUES (%s, %s, %s, %s) RETURNING id', 
            (put_req.nombre, put_req.tipo, put_req.ip, put_req.ubicacion,)
        )

        generated_id = self.cursor.fetchone()["id"]
        self.conn.commit()

        logging.info(f'Equipo {put_req.nombre} creado con id {generated_id}')

        return generated_id

    def get_by_id(self, id):
        self.cursor.execute('SELECT * FROM equipos WHERE id = %s', (id,))
        row = self.cursor.fetchone()

        if row == None:
            return None

        return Equipo(**dict(row))

    def put(self, id, nombre, tipo, ip, ubicacion):
        try:
            self.cursor.execute('''
                UPDATE equipos
                SET nombre = %s, tipo = %s, ip = %s, ubicacion = %s
                WHERE id = %s;
            ''', (nombre, tipo, ip, ubicacion, id,)
            )

            if self.cursor.rowcount == 0:
                return False

            self.conn.commit()
            logging.info(f"Equipo con id: {id} actualizado")
            
            return True
        except Exception as e:
            logging.error(f'Error en la base de datos {e}')
            return None
    
    def delete(self, id):
        try:
            self.cursor.execute('''
                DELETE FROM equipos WHERE id = %s;
            ''', (id,))

            if self.cursor.rowcount == 0:
                return False
            
            self.conn.commit()
            logging.info(f"Equipo con id: {id} borrado")

            return True
        except Exception as e:
            logging.error(f'Error en la base de datos {e}')
            return None

    def lista(self):
        self.cursor.execute('''
            SELECT * FROM tecnicos;
        ''')

        return self.cursor.fetchall()