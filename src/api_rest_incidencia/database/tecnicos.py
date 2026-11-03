from api_rest_incidencia.models.tecnico import Tecnico
from sqlite3 import Connection
import logging

class HanddlerTecnicoDB:
    def __init__(self, conn:Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    def create(self, Tecnico:Tecnico):
        self.cursor.execute(
            'INSERT INTO tecnicos (nombre, especialidad, email) VALUES (%s, %s, %s) RETURNING id', 
            (Tecnico.nombre, Tecnico.especialidad, Tecnico.email,)
        )

        generated_id = self.cursor.fetchone()[0]
        self.conn.commit()

        Tecnico.id = generated_id

        logging.info(f'Técnico {Tecnico.nombre} creado con id {generated_id}')

        return Tecnico

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