# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# ⚠️ Cambia esta línea con tu contraseña y puerto (usa 5432 o 5433 según sea tu caso)
DATABASE_URL = "postgresql://postgres:laura13@localhost:5433/proyecto"

# Creamos el engine
engine = create_engine(DATABASE_URL)

# Crea una sesión (opcional, para consultar datos después)
SessionLocal = sessionmaker(bind=engine)

# Crear todas las tablas definidas en models.py
def crear_tablas():
    Base.metadata.create_all(bind=engine)
