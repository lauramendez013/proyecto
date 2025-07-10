from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Hotel, Base
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# Permitir acceso desde el frontend (HTML)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción, usa ["http://localhost:8000"] o el dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#get 
@app.get("/hoteles/")
def listar_hoteles(db: Session = Depends(get_db)):
    return db.query(Hotel).all()

#crear hotel con BaseModel  
class HotelCreate(BaseModel):
    nombre: str
    ciudad: str

@app.post("/hoteles/")
def crear_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    nuevo_hotel = Hotel(nombre=hotel.nombre, ciudad=hotel.ciudad)
    db.add(nuevo_hotel)
    db.commit()
    db.refresh(nuevo_hotel)
    return nuevo_hotel

@app.put("/hoteles/{hotel_id}")
def actualizar_hotel(hotel_id: int, hotel: HotelCreate, db: Session = Depends(get_db)):
    hotel_existente = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_existente:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    hotel_existente.nombre = hotel.nombre
    hotel_existente.ciudad = hotel.ciudad
    db.commit()
    db.refresh(hotel_existente)
    return hotel_existente

@app.delete("/hoteles/{hotel_id}")
def eliminar_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_existente = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_existente:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    db.delete(hotel_existente)
    db.commit()
    return {"detail": "Hotel eliminado exitosamente"}

