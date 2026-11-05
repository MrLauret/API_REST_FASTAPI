from api_rest_incidencia.models.tecnico import Tecnico
from sqlite3 import Connection
import logging

class handlerTecnicoDB:
    def __init__(self, conn:Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    def create(self, put_req):
        self.cursor.execute(
            'INSERT INTO tecnicos (nombre, especialidad, email) VALUES (%s, %s, %s) RETURNING id', 
            (put_req.nombre, put_req.especialidad, put_req.email,)
        )

        generated_id = self.cursor.fetchone()["id"]
        self.conn.commit()

        logging.info(f'Técnico {put_req.nombre} creado con id {generated_id}')

        return generated_id

    def get_by_id(self, id):
        self.cursor.execute('SELECT * FROM tecnicos WHERE id = %s', (id,))
        row = self.cursor.fetchone()

        if row == None:
            return None

        return Tecnico(**dict(row))

    def put(self, id, nombre, email, especialidad):
        try:
            self.cursor.execute('''
                UPDATE tecnicos
                SET nombre = %s, email = %s, especialidad = %s
                WHERE id = %s;

            ''', (nombre, email, especialidad, id,)
            )

            if self.cursor.rowcount == 0:
                return False

            self.conn.commit()
            logging.info(f"Tecnico con id: {id} actualizado")
            
            return True
        except Exception as e:
            logging.error(f'Error en la base de datos {e}')
            return None
    
    def delete(self, id):
        try:
            self.cursor.execute('''
                DELETE FROM tecnicos WHERE id = %s;
            ''', (id,))

            if self.cursor.rowcount == 0:
                return False
            
            self.conn.commit()
            logging.info(f"Tecnico con id: {id} borrado")

            return True
        except Exception as e:
            logging.error(f'Error en la base de datos {e}')
            return None

    def lista(self):
        self.cursor.execute('''
            SELECT * FROM tecnicos;
        ''')

        return self.cursor.fetchall()