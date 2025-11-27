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
