#Heredamos de la clase 'Node'
extends Node

#Declaramos la localizacion del archivo 'JSON' con la 'url' base
var url_base_path="res://base_url.json"

#Configuramos la 'url' para obtener las ultimas medidas
var url = ""

#Creamos las 'signal' para transmitir datos
signal initial_status_em_300_th_915_1(message_to_emit)
signal initial_status_em_300_th_915_2(message_to_emit)

signal initial_status_em_500_lgt_915m(message_to_emit)
signal initial_status_em_500_co2_915m(message_to_emit)
signal initial_status_em_500_smtc_915m(message_to_emit)

signal initial_status_sph01lb_1(message_to_emit)
signal initial_status_sph01lb_2(message_to_emit)

signal initial_status_wts_506_915m(message_to_emit)

#Instanciamos el componente 'http'
@onready var http_request = $HTTPRequest

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

# Called when the node enters the scene vtree for the first time.
func _ready() -> void:
	
	print("Estoy listo")
	
	#Obtenemos la 'url' base
	var url_base=load_json_file(url_base_path)
		
	#Ensamblamos la 'url' completa
	url= "http://" + url_base + ":9090/get-last-measures"
		
	#Hacemos la conexion declarando la funcion que se ejecuta cuando la peticion completada
	http_request.request_completed.connect(_on_request_completed)	
	
	#Enviamos la peticion
	send_request()
	

#Esta funcion envia la peticion
func send_request():
	
	#Declaramos las cabeceras 
	var headers = ["Content-Type: application/json"]
	http_request.request(url, headers, HTTPClient.METHOD_GET)
	
#Esta funcion se ejecuta al finalizar la peticion
func _on_request_completed(results, response_code, headers, body):
	
	#recibimos y devolvemos un JSON
	var devices_status = JSON.parse_string(body.get_string_from_utf8())
		
	#Iteramos en la respuesta
	for device in devices_status:
				
		#Verificamos por 'topic'
		match device["topic"]:
			"EM300-TH-915M-1":
				#Arreglamos el mensaje
				var message = {
					"temperature": device["temperature"],
					"humidity": device["humidity"]
					}
				#Emitimos la 'signal'
				initial_status_em_300_th_915_1.emit(str(message))
			"EM300-TH-915M-2":
				#Arreglamos el mensaje
				var message = {
					"temperature": device["temperature"],
					"humidity": device["humidity"]
					}
				#Emitimos la 'signal'
				initial_status_em_300_th_915_2.emit(str(message))
			"EM500-LGT-915M":
				#Arreglamos el mensaje
				var message = {
					"illumination": device["illumination"]
					}
				#Emitimos la 'signal'
				initial_status_em_500_lgt_915m.emit(str(message))			
			"EM500-CO2-915M":
				#Arreglamos el mensaje
				var message = {
					"temperature": device["temperature"],
					"humidity": device["humidity"],
					"CO2": device["co2"],
					"ap": device["pressure"],
					}
				#Emitimos la 'signal'
				initial_status_em_500_co2_915m.emit(str(message))			
			"EM500-SMTC-915M":
				#Arreglamos el mensaje
				var message = {
					"temperature": device["temperature"],
					"conductivity": device["conductivity"],
					"Soil Moisture": device["soil_moisture"],
					}
				#Emitimos la 'signal'
				initial_status_em_500_smtc_915m.emit(str(message))	
						
			"SPH01-LB-1":
				#Arreglamos el mensaje
				var message = {
					"TEMP_SOIL": device["temperature"],
					"PH1_SOIL": device["ph"]
					}
				#Emitimos la 'signal'
				initial_status_sph01lb_1.emit(str(message))					
			"SPH01-LB-2":
				#Arreglamos el mensaje
				var message = {
					"TEMP_SOIL": device["temperature"],
					"PH1_SOIL": device["ph"]
					}
				#Emitimos la 'signal'
				initial_status_sph01lb_2.emit(str(message))							
			"WTS506-915M":
				#Arreglamos el mensaje
				var message = {
					"battery": device["battery"],
					"temperature": device["temperature"],
					"humidity": device["humidity"],
					"wind_speed": device["wind_speed"],
					"wind_direction": device["wind_direction"],
					"pressure": device["pressure"],
					}
				#Emitimos la 'signal'
				initial_status_wts_506_915m.emit(str(message))	
				
