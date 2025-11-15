from fastapi import FastAPI, HTTPException, Depends
from typing import Dict, Type, Optional
from enum import Enum
from datetime import datetime
from .models import BookBase as PydanticBookBase # Renombramos para evitar conflicto

# agregar tiendas nuevas aca
class Tienda(str, Enum):
    FALABELLA = "falabella"
    BUSCALIBRE = "buscalibre" 
    ANTARTICA = "antartica"
    MIRALIBROS = "miralibros"
    FERIACHILENA = "feriachilena"

class BookCreate(PydanticBookBase):
    precio: int
    precio_tarjeta: Optional[int] = None
    pass

class BookService:
    def __init__(self, db_engine):
        self.engine = db_engine
        self.table_mapping = {
            Tienda.FALABELLA: "falabella",
            Tienda.BUSCALIBRE: "buscalibre",
            Tienda.ANTARTICA: "antartica", 
            Tienda.MIRALIBROS: "miralibros",
            Tienda.FERIACHILENA: "feriachilena"
        }
    
    async def create_book(self, book: BookCreate, tienda: Tienda):
        table_name = self.table_mapping[tienda]
        
        async with self.engine.begin() as conn:
            await self._upsert_libro_maestro(conn, book)
            await conn.execute(
                text(f"""
                    INSERT INTO {table_name} 
                    (isbn, ultimo_precio, link, fecha_actualizacion)
                    VALUES (:isbn, :precio, :link, :fecha_actualizacion)
                    ON CONFLICT (isbn) DO UPDATE SET
                        ultimo_precio = EXCLUDED.ultimo_precio,
                        link = EXCLUDED.link,
                        fecha_actualizacion = EXCLUDED.fecha_actualizacion
                """),
                {
                    "isbn": book.isbn,
                    "precio": book.precio,
                    "link": book.link,
                    "fecha_actualizacion": book.fecha_actualizacion
                }
            )
            await self._registrar_historico(conn, book, tienda)

def get_book_service():
    return BookService(db_engine)

@app.post("/books/{tienda}")
async def create_book(
    tienda: Tienda,
    book: BookCreate,
    service: BookService = Depends(get_book_service)
):
    """
    Crea o actualiza un libro en la tienda especificada
    """
    try:
        await service.create_book(book, tienda)
        return {
            "status": "success", 
            "tienda": tienda.value,
            "isbn": book.isbn,
            "message": "Libro procesado correctamente"
        }
    except Exception as e:
        raise HTTPException(500, f"Error procesando libro: {str(e)}")