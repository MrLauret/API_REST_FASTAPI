from pydantic import BaseModel

class Equipo(BaseModel):
    def __init__(self, nombre:str, tipo:str, ip:str, ubicacion:str, id=None):
        self.id = id | None
        self.nombre = nombre
        self.tipo = tipo
        self.ip = ip
        self.ubicacion = ubicacion
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "ip": self.ip,
            "ubicacion": self.ubicacion
        }