#Con esta libreria manejamos el contexto de forma asincrona
from contextlib import asynccontextmanager

#Importamos 'fastapi'
from fastapi import FastAPI

#Importamos las librerias de SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Importamos las lobrerias utilitarias
import os
from dotenv import load_dotenv

#Importamos el utilitario de conexion 'MQTT'
from .mqtt_manager import MQTTClient

#Importamos las rutas
from .routes import router

#Cargamos variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

#Instanciamos el cliente 'MQTT'
mqtt_client = MQTTClient(
    os.getenv("MQTT_BROKER"),
    int(os.getenv("MQTT_PORT")),
    os.getenv("MQTT_TOPICS").split(","),
    os.getenv("MQTT_USERNAME"),
    os.getenv("MQTT_PASSWORD"),
    session
    )


#Gestionamos los eventos de inicio y finalizacion de la aplicacion esto sirve para abrir o detener el cliente 'MQTT'
@asynccontextmanager
async def lifespan(app: FastAPI):

    #Nos conectamos al 'broker MQTT'
    mqtt_client.connect_mqtt()    

    #Nos subscribimos a los 'topics'
    mqtt_client.subscribe()

    # Almacenar la instancia de MQTTClient en el estado de la aplicación
    app.state.mqtt_client = mqtt_client

    # Start the MQTT client
    mqtt_client.start()
    yield
    # Stop the MQTT client
    mqtt_client.stop()
    
#Creamos la aplicacion
#Almacenamos el 'lifespan' dentro del estado de la aplicacion para poderlo usar dese 'routes'
app = FastAPI(lifespan=lifespan)

# Incluir las rutas
app.include_router(router)