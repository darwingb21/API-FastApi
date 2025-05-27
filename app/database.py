import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


#DB_HOST = os.getenv("DB_HOST", "localhost") #local
DB_HOST = os.getenv("DB_HOST", "bd") # Docker
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@{DB_HOST}:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

