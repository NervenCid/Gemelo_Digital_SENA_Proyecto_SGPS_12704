#Heredamos de la clase 'Node'
extends Node

#Declaramos la localizacion del archivo 'JSON' con la 'url' base
var url_base_path="res://base_url.json"

#Configuramos la conexion a 'websockets'
var websocket_url = ""

var socket := WebSocketPeer.new() #Instanciamos un socket

#Creamos las 'signal' para transmitir datos

signal message_from_em_300_th_915_1(message_to_emit)
signal message_from_em_300_th_915_2(message_to_emit)

signal message_from_em_500_lgt_915m(message_to_emit)
signal message_from_em_500_co2_915m(message_to_emit)
signal message_from_em_500_smtc_915m(message_to_emit)

signal message_from_sph01lb_1(message_to_emit)
signal message_from_sph01lb_2(message_to_emit)

signal message_from_wts_506_915m(message_to_emit)

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


# Called when the node enters the scene tree for the first time.
func _ready():
	
	#Obtenemos la 'url' base
	var url_base=load_json_file(url_base_path)
		
	#Ensamblamos la 'url' completa
	websocket_url= "ws://" + url_base + ":9080/ws"
	
	#Validamos si hay un error de conexion
	if socket.connect_to_url(websocket_url) != OK:

		#Mostramos un mensaje de error
		print("Error de Conexion!!!")
		set_process(false)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	
	#Invocamos un 'poll' que se encarga de actualizar la conexion y recibir paquetes
	socket.poll()

	#Validamos que la conexion este abierta
	if socket.get_ready_state() == WebSocketPeer.STATE_OPEN:

		#Procedemos a revisar si se han recibido paquetes
		while socket.get_available_packet_count():			

			#Recibimos el paquete de informacion
			var packet = socket.get_packet().get_string_from_ascii()
												
			#Validamos
			if packet != "Conectando..." && packet != "Unable to connect!!!" && packet!=null: 	

				#Convertimos a JSON
				var JSONParsed = JSON.parse_string(packet)								
			
				#Repartimos a los 'display' segun el 'topis' que llegue			
				match JSONParsed["topic"]:
					"EM300-TH-915M-1":
						#Emitimos la 'signal'
						message_from_em_300_th_915_1.emit(JSONParsed["message"])
						print("Llego EM300-TH-915M-1")
					"EM300-TH-915M-2":
						#Emitimos la 'signal'
						message_from_em_300_th_915_2.emit(JSONParsed["message"])
						print("Llego EM300-TH-915M-2")
					"EM500-LGT-915M":
						#Emitimos la 'signal'
						message_from_em_500_lgt_915m.emit(JSONParsed["message"])
						print("Llego EM500-LGT-915M")
					"EM500-CO2-915M":
						#Emitimos la 'signal'
						message_from_em_500_co2_915m.emit(JSONParsed["message"])
						print("Llego EM500-CO2-915M")
					"EM500-SMTC-915M":
						#Emitimos la 'signal'
						message_from_em_500_smtc_915m.emit(JSONParsed["message"])
						print("Llego EM500-SMTC-915M")
					"SPH01-LB-1":
						#Emitimos la 'signal'
						message_from_sph01lb_1.emit(JSONParsed["message"])
						print("Llego SPH01-LB-1")
					"SPH01-LB-2":
						#Emitimos la 'signal'
						message_from_sph01lb_2.emit(JSONParsed["message"])
						print("Llego SPH01-LB-2")
					"WTS506-915M":
						#Emitimos la 'signal'
						message_from_wts_506_915m.emit(JSONParsed["message"])
						print("Llego WTS506-915M")

	#Validamos que se este tratando de conectar
	elif socket.get_ready_state() == WebSocketPeer.STATE_CONNECTING:

		#Este mensaje se muestra cuando se intenta conectar
		print("Conectando...")	

	else:

		#Tratamos de recuperar la conexion Validamos si hay un error de conexion
		if socket.connect_to_url(websocket_url) != OK:

			#Mostramos un mensaje de error
			print("Unable to connect!!!")
			set_process(false)
