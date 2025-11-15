from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):

    isbn: str
    titulo: str
    ultimo_precioint: int
    ultimo_precionm: Optional[int] = None
    portada: str
    link: str
    categoria: str
    fecha_actualizacion: datetime

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True