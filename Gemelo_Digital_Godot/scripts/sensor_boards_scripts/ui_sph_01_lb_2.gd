#Heredamos de la clase 'Control'
extends Control

#Llamamos al cliente de 'WebSockets'
@onready var WebSocketClient = get_node("../../../WebSocketClient")

#Llamamos al cliente de 'HTTP'
@onready var HTTPClientInitialStatus = get_node("../../../HTTPClient")

#Definimos las salidas de texto
@onready var temperature_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer/temperature_measure
@onready var ph_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer2/ph_measure

# Called when the node enters the scene tree for the first time.
func _ready():
	
	#Conectamos las 'signals'
	WebSocketClient.message_from_sph01lb_2.connect(_on_received_message)
	HTTPClientInitialStatus.initial_status_sph01lb_2.connect(_on_received_message)

#Escuchamos la 'signal'
func _on_received_message(msg):
	
	#Convertimos a JSON
	var message = JSON.parse_string(msg)

	#Mostramos en las cajas de texto
	temperature_measure_text_client.text = str(message["TEMP_SOIL"])
	ph_measure_text_client.text = str(message["PH1_SOIL"])
	
