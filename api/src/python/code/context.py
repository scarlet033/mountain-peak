from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

HTTP_HOST = config("HTTP_HOST", default="0.0.0.0")
HTTP_PORT = config("HTTP_PORT", cast=int, default=5000)


VERSION = config("VERSION", default="1")
VERSION_FULL = config("VERSION_FULL", default="1.0.0000")
DEPLOYED_PREFIX = config("DEPLOYED_PREFIX", default='')

DB_PROCOTOL = config('DB_PROCOTOL', default='postgresql')
DB_HOST = config('DB_HOST', default='localhost')
DB_PORT = config('DB_PORT', cast=int, default=5432)
DB_SCHEMA = config('DB_SCHEMA', default='mountain')  # db name
DB_USER = config('DB_USER', default='user23')
DB_PASS = config('DB_PASS', cast=Secret, default="pwd23")
DB_URL = f"{DB_PROCOTOL}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_SCHEMA}"
DB_SQLALCHEMY_ECHO = config("DB_SQLALCHEMY_ECHO", cast=bool, default=False)

# docker run -d --network="host" --name postgis-container -e POSTGRES_PASSWORD=pwd23 -e POSTGRES_USER=user23 -e POSTGRES_DB=mountain postgis/postgis:15-3.3-alpine
# docker pull postgis/postgis:15-3.3-alpine