from fastapi import FastAPI
#from . import  database 
from .database import Base

from .database import engine
from .routes import users, auth, protected, products

# Configuración inicial
Base.metadata.create_all(bind=engine)
app = FastAPI()

# Incluir routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(protected.router)