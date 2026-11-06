# API REST de incidencias

API REST desarrollada con FastAPI para gestionar incidencias, equipos y técnicos. La persistencia se realiza en PostgreSQL mediante Psycopg 3.

## Requisitos

- Python 3.14 (versión indicada en `.python-version` y `pyproject.toml`).
- PostgreSQL accesible desde la máquina donde se ejecuta la API.
- `pip` y, para el servidor de desarrollo, Uvicorn.

## Instalación y configuración

1. Crea una base de datos y un usuario en PostgreSQL. Por ejemplo, desde `psql` como administrador:

     ```sql
     CREATE USER user_api WITH PASSWORD 'cambia_esta_clave';
     CREATE DATABASE api_db OWNER user_api;
     ```

2. Desde la raíz del proyecto, crea `.env` a partir de `.env.example` y configura la conexión:

     ```dotenv
     host="localhost"
     db_name="api_db"
     db_user="user_api"
     db_password="cambia_esta_clave"
     db_port="5432"
     ```

     Los nombres de las variables deben escribirse exactamente en minúsculas, tal como aparecen arriba. No compartas el archivo `.env` ni guardes contraseñas reales en el repositorio.

3. Crea un entorno virtual e instala el proyecto y Uvicorn:

     ```bash
     python3.14 -m venv .venv
     source .venv/bin/activate
     python -m pip install --upgrade pip
     python -m pip install -e . "uvicorn[standard]"
     ```

     En Windows, activa el entorno con `.venv\Scripts\activate`.

## Ejecutar la API

Desde la raíz del repositorio y con el entorno virtual activado:

```bash
python -m uvicorn api_rest_incidencia.main:app --app-dir src --reload
```

La API estará disponible en `http://127.0.0.1:8000`. FastAPI publica la documentación interactiva en:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Al iniciar la aplicación, se conecta a PostgreSQL y ejecuta los archivos SQL de `src/api_rest_incidencia/database/migrations/` en orden alfabético. Las tablas se crean si no existen.

## Pruebas

El proyecto incluye pruebas automatizadas bajo `tests/api` para validar los endpoints principales de la API usando `pytest` y un fixture mock para evitar depender directamente de PostgreSQL durante la ejecución de la prueba.

Para ejecutar la batería completa:

```bash
cd /home/user/Documents/Programming/API_REST_Incidencia
. .venv/bin/activate
python -m pytest tests/api -q
```

También puedes lanzar un archivo concreto:

```bash
python -m pytest tests/api/test_tecnicos.py -q
python -m pytest tests/api/test_equipos.py -q
python -m pytest tests/api/test_incidencias.py -q
```

Las pruebas cubren:

- listado, detalle, creación, actualización y borrado de técnicos
- listado, detalle, creación, actualización y borrado de equipos
- listado, detalle, creación, actualización, borrado, cierre y asignación de técnicos a incidencias

## Convenciones de la API

- Los recursos se sirven bajo `/api` y las rutas terminan en `/`.
- Los cuerpos y respuestas usan JSON, salvo que se indique lo contrario.
- Las respuestas de validación pueden ser `400` o `422`, según el error detectado por FastAPI.
- Los identificadores son enteros autogenerados por PostgreSQL.
- Los valores aceptados para `prioridad` son `baja`, `media`, `alta` y `critica`.
- Los valores aceptados para `estado` son `abierta`, `en proceso` y `cerrada`. La validación de `PUT` de incidencias no distingue mayúsculas y minúsculas.

## Endpoints

### Incidencias

#### `GET /api/incidencias/`

Devuelve la lista de incidencias. Cada elemento contiene `id`, `titulo`, `descripcion`, `prioridad`, `estado`, `equipo_id`, `tecnico_id`, `fecha_creacion` y `fecha_modificacion`.

#### `POST /api/incidencias/`

Crea una incidencia. El equipo indicado debe existir. Aunque `tecnico_id` admite `null`, la propiedad debe incluirse en el cuerpo.

```json
{
    "titulo": "No enciende el equipo",
    "descripcion": "El ordenador no responde al pulsar el botón de encendido",
    "prioridad": "alta",
    "estado": "abierta",
    "equipo_id": 1,
    "tecnico_id": null
}
```

Respuesta `201 Created`:

```json
{"id": 1}
```

Devuelve `404` si no existe el equipo indicado.

#### `GET /api/incidencias/{incidencia_id}/`

Obtiene una incidencia por identificador. Cuando se encuentra, la respuesta pretende incluir los mismos campos que la lista. Devuelve `404` si no existe.

#### `PUT /api/incidencias/{incidencia_id}/`

Reemplaza los datos editables de la incidencia. Deben enviarse todos los campos del siguiente cuerpo; `descripcion` y `tecnico_id` pueden ser `null`.

```json
{
    "titulo": "No enciende el equipo",
    "descripcion": "Revisar fuente de alimentación",
    "prioridad": "media",
    "estado": "en proceso",
    "equipo_id": 1,
    "tecnico_id": 2
}
```

Devuelve `200` al editar, `400` si el estado o la prioridad no son válidos y `404` si no existe la incidencia, el equipo o el técnico indicado.

#### `PATCH /api/incidencias/{incidencia_id}/cerrar/`

Cambia el estado de la incidencia a `cerrada` y actualiza `fecha_modificacion`. No requiere cuerpo. La ruta devuelve `200` al completar la operación.

#### `PATCH /api/incidencias/{incidencia_id}/asignar_tecnico/`

Asigna un técnico existente a la incidencia. El cuerpo es:

```json
{"tecnico_id": 2}
```

El campo `tecnico_id` está definido como opcional en el esquema de entrada. La ruta devuelve el resultado del handler, que debería representar la incidencia actualizada.

#### `DELETE /api/incidencias/{incidencia_id}/`

Elimina una incidencia. Devuelve `200` con un mensaje de confirmación, `404` si no existe y `500` si ocurre un error en la base de datos.

### Equipos

Los campos de un equipo son `nombre`, `tipo`, `ip` y `ubicacion`.

#### `GET /api/equipos/`

Devuelve la lista de equipos.

#### `POST /api/equipos/`

Crea un equipo. Ejemplo de cuerpo:

```json
{
    "nombre": "PC recepción",
    "tipo": "Ordenador",
    "ip": "192.168.1.20",
    "ubicacion": "Recepción"
}
```

Respuesta `201 Created`: `{"id": 1}`.

#### `GET /api/equipos/{equipo_id}/`

Obtiene un equipo por identificador.

#### `PUT /api/equipos/{equipo_id}/`

Reemplaza los cuatro campos del equipo. Usa el mismo cuerpo que `POST`. Devuelve `200` si se actualiza y `404` si no se encuentra.

#### `DELETE /api/equipos/{equipo_id}/`

Elimina un equipo. Devuelve `200` con un mensaje de confirmación, `404` si no existe y `500` si ocurre un error en la base de datos.

### Técnicos

Los campos de un técnico son `nombre`, `email` y `especialidad`.

#### `GET /api/tecnicos/`

Devuelve la lista de técnicos.

#### `POST /api/tecnicos/`

Crea un técnico. Ejemplo de cuerpo:

```json
{
    "nombre": "Ana García",
    "email": "ana.garcia@example.com",
    "especialidad": "Sistemas"
}
```

Respuesta `201 Created`: `{"id": 1}`.

#### `GET /api/tecnicos/{tecnico_id}/`

Obtiene un técnico por identificador.

#### `PUT /api/tecnicos/{tecnico_id}/`

Reemplaza `nombre`, `email` y `especialidad`. Usa el mismo cuerpo que `POST`.

#### `DELETE /api/tecnicos/{tecnico_id}/`

Elimina un técnico. Devuelve `200` con un mensaje de confirmación, `404` si no existe y `500` si ocurre un error en la base de datos.

## Base de datos PostgreSQL

La conexión se abre durante el inicio de la aplicación con los cinco parámetros de `.env`: `host`, `db_name`, `db_user`, `db_password` y `db_port`. La conexión se cierra al apagar la aplicación.

Las migraciones crean estas tablas:

| Tabla | Columnas |
| --- | --- |
| `equipos` | `id` (`SERIAL PRIMARY KEY`), `nombre`, `tipo`, `ip`, `ubicacion` (texto, obligatorios) |
| `tecnicos` | `id` (`SERIAL PRIMARY KEY`), `nombre`, `email`, `especialidad` (texto, obligatorios) |
| `incidencias` | `id` (`SERIAL PRIMARY KEY`), `titulo` (texto, obligatorio), `descripcion` (texto, admite `NULL`), `prioridad`, `estado`, `equipo_id` (enteros/texto obligatorios según el esquema), `tecnico_id` (entero, admite `NULL`), `fecha_creacion` y `fecha_modificacion` (texto, obligatorios) |

Las columnas `equipo_id` y `tecnico_id` no tienen restricciones `FOREIGN KEY` en las migraciones actuales. La existencia de los registros relacionados se comprueba desde algunos handlers de la aplicación.

## Ejemplos con `curl`

Crear un equipo:

```bash
curl -X POST http://127.0.0.1:8000/api/equipos/ \
    -H 'Content-Type: application/json' \
    -d '{"nombre":"PC recepción","tipo":"Ordenador","ip":"192.168.1.20","ubicacion":"Recepción"}'
```

Listar incidencias:

```bash
curl http://127.0.0.1:8000/api/incidencias/
```

Cerrar una incidencia:

```bash
curl -X PATCH http://127.0.0.1:8000/api/incidencias/1/cerrar/
```

Eliminar un técnico:

```bash
curl -X DELETE http://127.0.0.1:8000/api/tecnicos/1/
```
