CREATE TABLE IF NOT EXISTS incidencias (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    prioridad TEXT NOT NULL,
    estado TEXT NOT NULL,
    equipo_id INTEGER NOT NULL,
    tecnico_id INTEGER,
    fecha_creacion TEXT NOT NULL,
    fecha_modificacion TEXT NOT NULL
)