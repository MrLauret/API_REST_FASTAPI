from pydantic import BaseModel

class Tecnico(BaseModel):
    def __init__(self, id:int, nombre:str, email:str, especialidad:str):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.especialidad = especialidad
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "especialidad": self.especialidad
        }