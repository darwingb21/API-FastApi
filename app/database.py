import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "") # Docker

engine = create_engine("postgresql://postgress:eK0BGy3vmfd6be9ZUz6xuqkNHLVE8ty5@dpg-d0qjh9emcj7s73e3g8l0-a/postgress_xgwp", pool_pre_ping=True)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

