#Heredamos de la clase 'Node'
extends Node

#Declaramos la localizacion del archivo 'JSON' con la 'url' base
var url_base_path="res://base_url.json"

#Configuramos la conexion
var websocket_url = ""
var socket := WebSocketPeer.new() #Instanciamos un socket

#Llamamos al cliente de 'HTTP'
@onready var HTTPClientInitialStatus = get_node("../HTTPClient")

#Cajas de texto para mostrar la ultima transmision recibida via MQTT
@onready var time_measure_text_client = $Last_transmission_received/VBoxContainer/HBoxTimeContainer/time_measure
@onready var sensor_topic_text_client = $Last_transmission_received/VBoxContainer/HBoxSensorContainer/sensor_topic
@onready var message_text_client = $Last_transmission_received/VBoxContainer/HBoxMessageContainer/message

#Cajas de texto para mostrar el estado de la estacion meteorologica
@onready var temperature_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer/temperature_measure
@onready var humidity_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer2/humidity_measure
@onready var wind_direction_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer3/wind_direction_measure
@onready var wind_speed_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer4/wind_speed_measure
@onready var pressure_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer5/pressure_measure

#Con esta funcion cargamos un archivo JSON
func load_json_file(filePath : String):
	
	#Validamos que el archivo exista
	if FileAccess.file_exists(filePath):
		
		#Abrimos el archivo
		var dataFile = FileAccess.open(filePath, FileAccess.READ)
		
		#Convertimos el contenido a 'JSON'
		var parsedResult = JSON.parse_string(dataFile.get_as_text())
		
		#Validamos y retornamos
		if parsedResult is Dictionary:
			return parsedResult["base_url"]
		else:
			print("Archivo defectuoso")
		
	else:
		
		print("El archivo 'URL_base.json' no fue encontrado")

#Con esta funcion mostramos los datos recibidos a traves del socket
func log_message(message):

	message_text_client.text = message

	#Conectamos las 'signals'
	HTTPClientInitialStatus.initial_status_wts_506_915m.connect(_on_received_message)
	
	if message != "Conectando..." && message != "Unable to connect!!!": 			
		
		#Convertimos a JSON
		var result = JSON.parse_string(message)
	
		#Ensamblamos un 'string' que contiene la marca de tiempo de recepcion del mensaje
		#var time = "[color=#aaaaaa] %s [/color]" % Time.get_time_string_from_system()
	
		#Mostramos el mensaje en la caja de texto en la interfaz de usuario
		#text_client.text= time + message
		time_measure_text_client.text = Time.get_time_string_from_system()
		sensor_topic_text_client.text = result["topic"]
		message_text_client.text = result["message"]
		
		#Validamos si llego informacion de la estacion metereologica
		if result["topic"] == "WTS506-915M":
			var weather_data = JSON.parse_string(result["message"])
			temperature_measure_text_client.text = str(weather_data["temperature"]) 			
			humidity_measure_text_client.text = str(weather_data["humidity"])
			wind_direction_measure_text_client.text = str(weather_data["wind_direction"])
			wind_speed_measure_text_client.text = str(weather_data["wind_speed"])
			pressure_measure_text_client.text = str(weather_data["pressure"])
		
# Called when the node enters the scene tree for the first time.
func _ready():
	
	#Obtenemos la 'url' base
	var url_base=load_json_file(url_base_path)
		
	#Ensamblamos la 'url' completa
	websocket_url= "ws://" + url_base + ":9080/ws"
	
	#Validamos si hay un error de conexion
	if socket.connect_to_url(websocket_url) != OK:

		#Mostramos un mensaje de error
		log_message("Unable to connect.")
		set_process(false)


#Esta funcion define lo que sucede una diferencia de tiempo entre 'frame' y 'frame'
func _process(_delta):

	#Invocamos un 'poll' que se encarga de actualizar la conexion y recibir paquetes
	socket.poll()

	#Validamos que la conexion este abierta
	if socket.get_ready_state() == WebSocketPeer.STATE_OPEN:

		#Procedemos a revisar si se han recibido paquetes
		while socket.get_available_packet_count():			

			#Mostramos en la interfaz
			log_message(socket.get_packet().get_string_from_ascii())

	#Validamos que se este tratando de conectar
	elif socket.get_ready_state() == WebSocketPeer.STATE_CONNECTING:

		#Este mensaje se muestra cuando se intenta conectar
		log_message("Conectando...")	

	else:

		#Tratamos de recuperar la conexion Validamos si hay un error de conexion
		if socket.connect_to_url(websocket_url) != OK:

			#Mostramos un mensaje de error
			log_message("Unable to connect!!!")
			set_process(false)
	
	
#Escuchamos la 'signal'
func _on_received_message(msg):
	
	#Convertimos a JSON
	var message = JSON.parse_string(msg)

	#Mostramos en las cajas de texto
	temperature_measure_text_client.text = str(message["temperature"])
	humidity_measure_text_client.text = str(message["humidity"])
	wind_direction_measure_text_client.text = str(message["wind_direction"])
	wind_speed_measure_text_client.text = str(message["wind_speed"])
	pressure_measure_text_client.text = str(message["pressure"])
	
	
#Esta funcion cierra el socket
func _exit_tree():
	socket.close()
