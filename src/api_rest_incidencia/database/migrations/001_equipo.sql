CREATE TABLE IF NOT EXISTS equipos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    ip TEXT NOT NULL,
    ubicacion TEXT NOT NULL
)
