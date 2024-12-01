#Importamos el enrutador, las librerias de 'WebSocket' y de inyeccion de dependencias
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

#Instanciamos el enrutador
router = APIRouter()

#Creamos la ruta '/'
#Algo curioso es que el 'async' funciona aqui sin usar 'asyncio'
@router.get("/")
async def read_root():
    return {"message": "Servidor de Websockets en linea"}

#Declaramos la ruta de 'websockets'
@router.websocket_route("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    #Esperamos a que se acepte la conexion
    await websocket.accept() 

    #Capturamos el estado de la aplicacion
    mqtt_client=websocket.app.state.mqtt_client
            
    try:
        while True:

            #Agregamos el cliente
            mqtt_client.add_websocket_client(websocket)
           
            #Recibimos los datos desde el 'websocket'
            data=await websocket.receive_text() 
            #print(data)

            #Publicamos un mensaje al 'topic'
            mqtt_client.publish("Greetings_From_Digital_Twin", data)
            

    except WebSocketDisconnect:

        #Quitamos el cliente en caso de desconexion
        print("Hubo un error de conexion")
        mqtt_client.remove_websocket_client(websocket)
