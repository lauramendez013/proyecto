# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

# Declaramos el ORM base
Base = declarative_base()

# Tabla Hotel
class Hotel(Base):
    __tablename__ = "hotel"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)

    def __repr__(self):
        return f"<Hotel(id={self.id}, nombre='{self.nombre}', ciudad='{self.ciudad}')>"

class Habitacion(Base):
    __tablename__ = "habitacion"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey("hotel.id"))
    tipo = Column(String, nullable=False)  # estándar, premium, VIP
    capacidad = Column(Integer, nullable=False)

    hotel = relationship("Hotel", back_populates="habitaciones")
    disponibilidades = relationship("Disponibilidad", back_populates="habitacion")


class Disponibilidad(Base):
    __tablename__ = "disponibilidad"
    id = Column(Integer, primary_key=True)
    habitacion_id = Column(Integer, ForeignKey("habitacion.id"))
    fecha = Column(Date, nullable=False)
    disponible = Column(Boolean, default=True)

    habitacion = relationship("Habitacion", back_populates="disponibilidades")


class Tarifa(Base):
    __tablename__ = "tarifa"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey("hotel.id"))
    tipo_habitacion = Column(String, nullable=False)
    temporada = Column(String, nullable=False)  # alta o baja
    personas_min = Column(Integer, nullable=False)
    personas_max = Column(Integer, nullable=False)
    valor_noche = Column(Float, nullable=False)
