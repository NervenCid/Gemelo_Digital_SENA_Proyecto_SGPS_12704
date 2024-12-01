#Importamos 'fastapi'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#Importamos las rutas
from .routes import router
   
#Creamos la aplicacion
app = FastAPI()

# Configuración de CORS para permitir cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Incluir las rutas
app.include_router(router)
