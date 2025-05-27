# Implementacion de API usando FastAPI

### Ejecutar la API y la base de datos Postgress con docker

`> docker-compose up -d`

### Link del Deploy en Renders

https://api-fastapi-weqt.onrender.com/docs#/


### Environment local setup

1. `> python -m venv venv`
2. `> venv\Scripts\activate`
3. `> python -m pip install --upgrade pip`
4. `> pip install -r requirements.txt`

### Run Unitary Test

`pytest tests/ -v`

### Run API local

`uvicorn app.main:app --reload`

Ajustar la variable de entorno DATABASE_URL a una direccion de BD en local
     
                

                
