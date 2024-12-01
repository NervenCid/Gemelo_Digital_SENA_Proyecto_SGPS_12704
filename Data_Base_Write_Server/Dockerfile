#Esto es un comentario

#Indicamos que se necesita una version de Python especifica
#Para mas informacion: https://hub.docker.com/_/python
FROM python:3.11

#Indicamos la ubicacion del proyecto DENTRO del contenedor (no dentro de la maquina)
WORKDIR /app

#Copiamos el archivo 'requirements.txt' DENTRO DEL CONTENEDOR
COPY requirements.txt requirements.txt

#Instalamos via 'pip' los requerimientos dentro de 'requirements.txt'
RUN pip3 install -r requirements.txt

#Copiamos TODOS los archivos del directorio actual al directorio de trabajo del CONTENEDOR
COPY . .

# Expose the port on which the application will run
EXPOSE 9085

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "9085"]