from fastapi import FastAPI
from .database import Base
import sys

from .database import engine
from .routes import users, auth, products

def create_app():
    app = FastAPI(

        title="Teste de Codificação",  # Nombre de tu API
        description="Una API creada con FastAPI para gestionar clientes, productos y envios",
    )
    
    # Configuración de rutas
    app.include_router(users.router)
    app.include_router(products.router)
    app.include_router(auth.router)

    return app

# Solo crear tablas si no estamos en modo de prueba
if "pytest" not in sys.modules:
    Base.metadata.create_all(bind=engine)

app = create_app()