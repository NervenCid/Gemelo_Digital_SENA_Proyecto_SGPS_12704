#Importamos la libreria 'mqtt'
from paho.mqtt import client as mqtt_client

#Importamos las lobrerias utilitarias
import random
import json
from datetime import datetime
import logging

# Configuración del logger para que solo muestre los logs en consola
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO  # Nivel de logs que se mostrarán en la consola (puede ser DEBUG, INFO, WARNING, etc.)
)

logger = logging.getLogger("Data_base_writing")

#Importamos los modelos de los sensores
from .models import Em300Sensor, Em300Measure, Em500Sensor, Em500Measure, WeatherStation, WeatherStationMeasure, SPH01LBSensor, SPH01LBMeasure

#La siguiente clase gestiona el cliente 'MQTT'
class MQTTClient:

    #Constructor
    def __init__(self, broker, port, topics, mqtt_username, mqtt_password, session):

        #Parametros
        self.broker = broker
        self.port = port
        self.topics = topics
        self.mqtt_user = mqtt_username
        self.mqtt_password = mqtt_password   
        self.client = self.connect_mqtt()     
        self.websocket_clients = [] 
        self.session = session
        
    #Con este metodo conectamos a 'MQTT'
    def connect_mqtt(self):

        # Generate a Client ID with the subscribe prefix.
        client_id = f'subscribe-{random.randint(0, 100)}'

        #Esta funcion se dispara con la conexion
        def on_connect(client, userdata, flags, reason_code, properties):

            #Validamos los estados de la conexion
            if flags.session_present:
                print(flags)
            if reason_code == 0:
                print("success!!")
            if reason_code > 0:
                # error processing
                print("error!!: ", reason_code)
        
        #Creamos un cliente
        client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id)
        client.username_pw_set(self.mqtt_user, self.mqtt_password)

        #Pasamos al cliente la funcion de validacion de conexion
        client.on_connect = on_connect

        #Pasamos el 'callback' de recepcion de mensajes
        client.on_message = self.on_message
    
        #Realizamos la conexion al 'broker'
        client.connect(self.broker, self.port)

        #Retornamos el cliente
        return client
    
    #Con este metodo no suscribimos al 'topic'
    def subscribe(self):

        #Subscribimos a los 'topic'
        for topic in self.topics:
            print("Subscribiendo a: ", topic)
            self.client.subscribe(topic)
            
    #Este es el 'callback' que se ejecuta al recibir un mensaje
    def on_message(self, client, userdata, msg):

        #Mostramos el estado
        print(f"Mensaje recibido: `{msg.payload.decode()}` , del 'topic': `{msg.topic}`")
        logger.info(f"Mensaje recibido: `{msg.payload.decode()}` , del 'topic': `{msg.topic}`")

        #Validamos y Guardamos en la base de datos
        if msg.payload.decode():
            self.save_on_database(json.loads(msg.payload.decode()), msg.topic)
        else:
            #Mostramos una advertencia
            print(f"Advertencia mensaje vacio del topic: `{msg.topic}`")
            logger.info(f"Advertencia mensaje vacio del topic: `{msg.topic}`")

    #Este metodo guarda el mensaje recibido en la base de datos
    def save_on_database(self, message, topic):

        #Buscamos en los sensores registrados
        query_em300 = self.session.query(Em300Sensor).filter(Em300Sensor.topic == topic)
        query_em500 = self.session.query(Em500Sensor).filter(Em500Sensor.topic == topic)
        query_weather_station = self.session.query(WeatherStation).filter(WeatherStation.topic == topic)
        query_sph01lb = self.session.query(SPH01LBSensor).filter(SPH01LBSensor.topic == topic)

         # Unir todas las consultas
        combined_query = query_em300.union_all(query_em500).union_all(query_weather_station).union_all(query_sph01lb)

        # Ejecutar la consulta y obtener el primer resultado
        sensor_data = combined_query.first()

        #Validamos que el sensor exista en la base de datos
        if sensor_data == None:
            print("No existe el sensor")
            return

        #Empaquetamos segun el sensor
        if sensor_data.model == "EM300-TH-915M":
            
            measure = Em300Measure(
                timestamp = datetime.now(),
                sensor_id = sensor_data.sensor_id,
                temperature = message["temperature"],
                humidity = message["humidity"]
            )
            self.session.add(measure)

        elif sensor_data.model == "EM500-SMTC-915M":

            measure = Em500Measure(
                timestamp = datetime.now(),
                sensor_id = sensor_data.sensor_id,
                temperature = message["temperature"],
                humidity = 0,
                pressure = 0,
                co2 = 0,
                illumination = 0,
                conductivity = message["conductivity"],
                soil_moisture = message["Soil Moisture"]
            )
            self.session.add(measure)

        elif sensor_data.model == "EM500-LGT-915M":

            measure = Em500Measure(
                timestamp = datetime.now(),
                sensor_id = sensor_data.sensor_id,
                temperature = 0,
                humidity = 0,
                pressure = 0,
                co2 = 0,
                illumination = message["illumination"],
                conductivity = 0,
                soil_moisture = 0
            )
            self.session.add(measure)

        elif sensor_data.model == "EM500-CO2-915M":

            measure = Em500Measure(
                timestamp = datetime.now(),
                sensor_id = sensor_data.sensor_id,
                temperature = message["temperature"],
                humidity = message["humidity"],
                pressure = message["ap"],
                co2 = message["CO2"],
                illumination = 0,
                conductivity = 0,
                soil_moisture = 0
            )
            self.session.add(measure)

        elif sensor_data.model == "WTS506-915M":

            measure = WeatherStationMeasure(
                timestamp = datetime.now(),
                sensor_id = sensor_data.sensor_id,
                temperature = message["temperature"],
                humidity = message["humidity"],
                battery = message["battery"],
                wind_direction = message["wind_direction"],
                pressure = message["pressure"],
                wind_speed = message["wind_speed"],
            )
            self.session.add(measure)

        elif sensor_data.model == "SPH01-LB":

            measure = SPH01LBMeasure(
                timestamp = datetime.now(),
                sensor_id = sensor_data.sensor_id,
                temperature=message["TEMP_SOIL"],
                ph = message["PH1_SOIL"]
            )
            self.session.add(measure)

        #Guardamos
        print(f"Guardado para el sensor: {sensor_data.model}, con identificador de 'topic': {sensor_data.topic}, mediciones: {message}")
        logger.info(f"Guardado para el sensor: {sensor_data.model}, con identificador de 'topic': {sensor_data.topic}, mediciones: {message}")
        self.session.commit()

            
    #Iniciamos el cliente
    def start(self):
        print("Iniciando cliente")
        self.client.loop_start()

    #Detenemos el cliente
    def stop(self):
        print("Deteniendo cliente")
        self.client.loop_stop()
        self.client.disconnect()
       
