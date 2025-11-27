# FastAPI + PostgreSQL API para tabla `stages`

Este proyecto crea una API con **FastAPI** conectada a **PostgreSQL** para manejar la tabla `stages`.

## 1. Crear carpeta del proyecto

```bash
mkdir mi_api_fastapi
cd mi_api_fastapi
```
## 2. Crear entorno virtual
```bash
python3.12 -m venv venv
source venv/bin/activate
```

## 3. Instalar dependencias
```bash
pip install fastapi uvicorn psycopg2-binary sqlalchemy python-dotenv alembic
```

## 4. Crear estructura del proyecto
```bash
mkdir app
mkdir app/routers
touch app/main.py app/database.py app/models.py app/schemas.py app/routers/stages.py
touch .env
```
Estructura resultante:
```bash
mi_api_fastapi/
│── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│        └── stages.py
│── .env
```

## 5. Configurar variables de entorno
```bash
DB_URL=postgresql://tu_usuario:tu_contraseña@localhost:5432/tu_base
```

## 6. Conexión a la base de datos
Archivo: app/database.py
```bash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 7. Modelo SQLAlchemy
Archivo: app/models.py
```bash
from sqlalchemy import Column, Integer, String
from .database import Base

class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    n_factura = Column(String)
    detalle = Column(String, unique=True, index=True)
    file_url = Column(String, unique=True, index=True)
```

## 8. Schemas Pydantic
Archivo: app/schemas.py
```bash
from pydantic import BaseModel
from typing import Optional

class StageBase(BaseModel):
    n_factura: Optional[str] = None
    detalle: Optional[str] = None
    file_url: Optional[str] = None

class StageCreate(StageBase):
    pass

class Stage(StageBase):
    id: int

    class Config:
        orm_mode = True
```

## 9. Rutas (CRUD)
Archivo: app/routers/stages.py
```bash
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/stages", tags=["Stages"])

# Crear un stage
@router.post("/", response_model=schemas.Stage)
def create_stage(stage: schemas.StageCreate, db: Session = Depends(get_db)):
    db_stage = models.Stage(**stage.dict())
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage

# Obtener todos
@router.get("/", response_model=list[schemas.Stage])
def get_stages(db: Session = Depends(get_db)):
    return db.query(models.Stage).all()

# Obtener por ID
@router.get("/{stage_id}", response_model=schemas.Stage)
def get_stage(stage_id: int, db: Session = Depends(get_db)):
    stage = db.query(models.Stage).filter(models.Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Stage no encontrado")
    return stage

# Eliminar
@router.delete("/{stage_id}")
def delete_stage(stage_id: int, db: Session = Depends(get_db)):
    stage = db.query(models.Stage).filter(models.Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Stage no encontrado")
    db.delete(stage)
    db.commit()
    return {"message": "Stage eliminado correctamente"}
```


## 10. Archivo principal FastAPI
Archivo: app/main.py
```bash
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

```

## 11. Archivo principal FastAPI
```bash
uvicorn app.main:app --reload
```

Documentacion
Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

