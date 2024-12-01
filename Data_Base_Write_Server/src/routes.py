#Importamos el enrutador, las librerias de 'WebSocket' y de inyeccion de dependencias
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

#Instanciamos el enrutador
router = APIRouter()

#Creamos la ruta '/'
#Algo curioso es que el 'async' funciona aqui sin usar 'asyncio'
@router.get("/")
async def read_root():
    return {"message": "API de escritura de datos de dispositivos en linea"}

