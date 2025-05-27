import pytest
import os, sys
import time
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.main import create_app
from app.database import Base, engine, get_db


# Configuración para Docker PostgreSQL

DB_HOST = os.getenv("DB_HOST", "localhost")
#TEST_DB_URL = f"postgresql://test:test@{DB_HOST}:5433/test"
TEST_DB_URL = DATABASE_URL = "sqlite:///test.db"



@pytest.fixture
def db():
    engine = create_engine(TEST_DB_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def app():
    # Configuración especial para pruebas
    app = create_app()
    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(app):
    return TestClient(app)