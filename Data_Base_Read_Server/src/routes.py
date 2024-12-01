#Importamos el enrutador, las librerias de 'WebSocket' y de inyeccion de dependencias
from fastapi import APIRouter, Depends

#Importamos los modelos
from .models import *

#Importamos la sesion de la base de datos
from sqlalchemy.orm import Session
from .db import get_db

#Importamos los servicios
from .services import get_last_measurements_for_each_topic

#Instanciamos el enrutador
router = APIRouter()

#
import logging
import sys

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

def to_dict(obj):
    """
    Convierte un objeto SQLAlchemy en un diccionario.
    """
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

#Creamos la ruta '/'
#Algo curioso es que el 'async' funciona aqui sin usar 'asyncio'
@router.get("/")
async def read_root():
    return {"message": "API de consulta de datos dde sensores en linea"}

#Esta ruta permite obtener las ultimas mediciones de los sensores
@router.get("/get-last-measures")
async def get_last_measures(db: Session = Depends(get_db)):

    #Creamos una lista vacia
    last_measures = []

    #Devolvemos la ultima medida obtenida segun el 'topic' asiciado a cada dispositivo
    last_measures.extend(get_last_measurements_for_each_topic(db, Em300Sensor, Em300Measure))
    last_measures.extend(get_last_measurements_for_each_topic(db, Em500Sensor, Em500Measure))
    last_measures.extend(get_last_measurements_for_each_topic(db, SPH01LBSensor, SPH01LBMeasure))
    last_measures.extend(get_last_measurements_for_each_topic(db, WeatherStation, WeatherStationMeasure))

    #Retornamos al cliente
    return last_measures
    

