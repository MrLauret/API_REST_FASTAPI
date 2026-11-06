class MockEquipoDB:
    def __init__(self):
        self.equipos = [
            {"id": 1, "nombre": "servidor", "tipo": "hardware", "ip": "111.23.41.6", "ubicacion": "Madrid"}
        ]

    def lista(self):
        return self.equipos

    def get_by_id(self, equipo_id):
        for equipo in self.equipos:
            if equipo["id"] == equipo_id:
                return equipo
        return None

    def create(self, payload):
        nuevo_id = max(t["id"] for t in self.equipos) + 1
        equipo = {
            "id": nuevo_id,
            "nombre": payload.nombre,
            "tipo": payload.tipo,
            "ip": payload.ip,
            "ubicacion": payload.ubicacion
        }
        self.equipos.append(equipo)
        return nuevo_id

    def put(self, equipo_id, nombre, tipo, ip, ubicacion):
        for equipo in self.equipos:
            if equipo["id"] == equipo_id:
                equipo["nombre"] = nombre
                equipo["ubicacion"] = ubicacion
                equipo["ip"] = ip
                equipo["tipo"] = tipo
                return True
        return False

    def delete(self, equipo_id):
        for equipo in self.equipos:
            if equipo["id"] == equipo_id:
                self.equipos.remove(equipo)
                return True
        return False
