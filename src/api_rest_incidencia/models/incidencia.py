from enum import Enum
import datetime

class Prioridad(Enum):
    Baja = 'baja'
    Media = 'media'
    Alta = 'alta'
    Critica = 'critica'

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value == value.lower():
                    return member
        
        raise ValueError(f'"{value}" no es una prioridad válida')

    @staticmethod
    def check_valido(x):
        try:
            Prioridad(x.lower())
            return True
        except ValueError:
            raise ValueError(
                'Prioridad invalida'
            )

class Estado(Enum):
    Abierta = 'abierta'
    En_proceso = 'en_proceso'
    Cerrada = 'cerrada'

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value == value.lower():
                    return member
        
        raise ValueError(f'"{value}" no es un estado válido')

    @staticmethod
    def check_valido(x):
        try:
            Estado(x.lower())
            return True
        except:
            return False

class Incidencia():
    def __init__(
        self, id:int, titulo:str, descripcion:str, equipo_id:int, prioridad:Estado, estado=Estado('abierta'), tecnico_id=None): 
        
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.estado = estado
        self.equipo_id = equipo_id
        self.tecnico_id = tecnico_id
        self.fecha_creacion = datetime.datetime.now()
        self.fecha_modificacion = datetime.datetime.now()

    def cambiar_estado(self, nuevo_estado:Estado):
        self.estado = nuevo_estado
        self.fecha_modificacion = datetime.datetime.now()
    
    def cambiar_prioridad(self, nueva_prioridad:Prioridad):
        self.prioridad = nueva_prioridad
        self.fecha_modificacion = datetime.datetime.now()
    
    def asignar_tecnico(self, id):
        self.tecnico_id = id
        self.fecha_modificacion = datetime.datetime.now()
    
    def cerrar(self):
        self.estado = Estado('cerrada')
        self.fecha_modificacion = datetime.datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'prioridad': self.prioridad.value,
            'estado': self.estado.value,
            'equipo_id': self.equipo_id,
            'tecnico_id': self.tecnico_id,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_modificacion': self.fecha_modificacion.isoformat()
        }