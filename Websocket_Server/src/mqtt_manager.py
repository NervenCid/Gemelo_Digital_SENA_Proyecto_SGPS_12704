#Importamos la libreria 'mqtt'
from paho.mqtt import client as mqtt_client

#Importamos el enrutador las librerias de 'WebSocket'
from fastapi import WebSocket, WebSocketDisconnect

#Importamos las lobrerias utilitarias
import random
import asyncio
import json

#La siguiente clase gestiona el cliente 'MQTT'
class MQTTClient:

    #Constructor
    def __init__(self, broker, port, topics, mqtt_username, mqtt_password):

        #Parametros de la clase
        self.broker = broker
        self.port = port
        self.topics = topics
        self.mqtt_user = mqtt_username
        self.mqtt_password = mqtt_password   
        self.client = self.connect_mqtt()     
        self.websocket_clients = [] 
        
    #Con este metodo realizamos la conexion a 'MQTT'
    def connect_mqtt(self):

        # Generate a Client ID with the subscribe prefix.
        client_id = f'subscribe-{random.randint(0, 100)}'

        #Definimos el 'callback' de validacion de conexion
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

        #Nos subscribimos de forma iterativa
        for topic in self.topics:
            print("Subscribiendo a: ", topic)
            self.client.subscribe(topic)
            
    #Agregamos un cliente
    def add_websocket_client(self, websocket):
        self.websocket_clients.append(websocket)

    #Removemos el cliente
    def remove_websocket_client(self, websocket):
        self.websocket_clients.remove(websocket)

    #Este es el 'callback' que se ejecuta al recibir un mensaje
    def on_message(self, client, userdata, msg):

        print(f"Mensaje recibido: `{msg.payload.decode()}` , del 'topic': `{msg.topic}`")
        
        #Enviamos de forma asincrona lo recibido por 'MQTT' a todos los 'websockets' conectados
        asyncio.run(self.send_to_websockets(msg.topic, msg.payload.decode()))
            

    #Enviamos a cada cliente 'websocket' conectado
    async def send_to_websockets(self, topic, message):

        #Convertimos a JSON
        json_to_send = {
            "topic": topic,
            "message": message
        }

        #Enviamos a todos los clientes conectados
        for websocket in self.websocket_clients:
            await websocket.send_json(json_to_send)    
            

    #Con este metodo publicamos a 'MQTT'
    def publish(self, topic, msg):

        result = self.client.publish(topic, msg)

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Enviado el mensaje: `{msg}` al 'topic' `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    #Iniciamos el cliente
    def start(self):
        print("Iniciando cliente")
        self.client.loop_start()

    #Detenemos el cliente
    def stop(self):
        print("Deteniendo cliente")
        self.client.loop_stop()
        self.client.disconnect()
       
