from sqlalchemy import Column, Integer, String
from .database import Base

class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    n_factura = Column(String)
    detalle = Column(String, unique=True, index=True)
    file_url = Column(String, unique=True, index=True)
