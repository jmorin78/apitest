from fastapi import FastAPI
from .database import Base, engine
from .routers import stages

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(stages.router)

@app.get("/")
def read_root():
    return {"message": "API de stages funcionando 🚀"}
