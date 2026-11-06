class MockTecnicoDB:
    def __init__(self):
        self.tecnicos = [
            {"id": 1, "nombre": "Ana García", "email": "ana@example.com", "especialidad": "Sistemas"}
        ]

    def lista(self):
        return self.tecnicos

    def get_by_id(self, tecnico_id):
        for tecnico in self.tecnicos:
            if tecnico["id"] == tecnico_id:
                return tecnico
        return None

    def create(self, payload):
        nuevo_id = max(t["id"] for t in self.tecnicos) + 1
        tecnico = {
            "id": nuevo_id,
            "nombre": payload.nombre,
            "email": payload.email,
            "especialidad": payload.especialidad,
        }
        self.tecnicos.append(tecnico)
        return nuevo_id

    def put(self, tecnico_id, nombre, email, especialidad):
        for tecnico in self.tecnicos:
            if tecnico["id"] == tecnico_id:
                tecnico["nombre"] = nombre
                tecnico["email"] = email
                tecnico["especialidad"] = especialidad
                return True
        return False

    def delete(self, tecnico_id):
        for tecnico in self.tecnicos:
            if tecnico["id"] == tecnico_id:
                self.tecnicos.remove(tecnico)
                return True
        return False
