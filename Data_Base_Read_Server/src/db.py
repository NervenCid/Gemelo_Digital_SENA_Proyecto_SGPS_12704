# db.py

#Importamos las librerias de SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Importamos las lobrerias utilitarias
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Función para obtener la sesión de base de datos
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()