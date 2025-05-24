""" from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
#  uvicorn app.main:app --reload

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
print("======================")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() """

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env si existe (para desarrollo local)
# Esto es útil si no usas docker-compose y quieres probar la API localmente,
# o si quieres cargar variables de entorno específicas para tu entorno de desarrollo
load_dotenv()

# Recuperar la URL de la base de datos de las variables de entorno
# El segundo argumento es un valor por defecto si DATABASE_URL no está definida.
# Usamos 'db' como host, que es el nombre del servicio de Postgres en docker-compose.yml
# Si ejecutas la API fuera de Docker, cambia 'db' a 'localhost' o la IP de tu DB.
""" SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/postgres" # Valor por defecto para Docker Compose
) """

DB_HOST = os.getenv("DB_HOST", "localhost")
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@{DB_HOST}:5432/postgres"

# Crear el motor de la base de datos
# `pool_pre_ping=True` ayuda a manejar conexiones que podrían haberse cerrado
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Crear una clase base para los modelos declarativos de SQLAlchemy
Base = declarative_base()

# Configurar la sesión de la base de datos
# `autocommit=False` para que los cambios se confirmen explícitamente (commit)
# `autoflush=False` para que la sesión no vacíe automáticamente
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

