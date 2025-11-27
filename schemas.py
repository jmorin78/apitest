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
