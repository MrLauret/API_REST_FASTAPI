
class MockincidenciaDB:
    def __init__(self):
        self.incidencias = [{
            "id": 1,
            "titulo": "pc roto",
            "descripcion": "no va",
            "prioridad": "baja",
            "estado": "En proceso",
            "equipo_id": "1",
            "tecnico_id": "1",
            "fecha_creación": "hoy",
            "fecha_modificacion": "hoy"
        }]

    def lista(self):
        return self.incidencias

    def get_by_id(self, incidencia_id):
        for incidencia in self.incidencias:
            if incidencia["id"] == incidencia_id:
                return incidencia
        return False

    def create(self, payload):
        nuevo_id = max(t["id"] for t in self.incidencias) + 1
        incidencia = {
            "id": 2,
            "titulo": payload.titulo,
            "descripcion": payload.descripcion,
            "prioridad": payload.descripcion,
            "estado": payload.estado,
            "equipo_id": payload.equipo_id,
            "tecnico_id": payload.tecnico_id,
            "fecha_creación": "ahora",
            "fecha_modificacion": "ahora"
        }
        self.incidencias.append(incidencia)
        return nuevo_id

    def put(self, incidencia_id, titulo, descripcion, prioridad, estado, equipo_id, tecnico_id):
        for incidencia in self.incidencias:
            if incidencia["id"] == incidencia_id:
                incidencia["titulo"] = titulo
                incidencia["descripcion"] = descripcion
                incidencia["prioridad"] = prioridad
                incidencia["estado"] = estado
                incidencia["equipo_id"] = equipo_id
                incidencia["tecnico_id"] = tecnico_id
                incidencia["fecha_modificacion"] = "ahora"
                return True
        return False

    def delete(self, incidencia_id):
        incidencia = self.get_by_id(incidencia_id)
        if not incidencia:
            return False
        
        self.incidencias.remove(incidencia)
        return True
    
    def asignar_tecnico(self, id, tecnico_id):
        incidencia = self.get_by_id(id)
        if not incidencia:
            return False
        
        incidencia["tecnico_id"] = tecnico_id
        return True
    
    def cerrar(self, id):
        incidencia = self.get_by_id(id)
        if not incidencia:
            return False
        
        incidencia["estado"] = "cerrada"
        return True