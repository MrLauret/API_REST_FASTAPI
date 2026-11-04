class Equipo():
    def __init__(self, id:int, nombre:str, tipo:str, ip:str, ubicacion:str):
        self.id = id
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