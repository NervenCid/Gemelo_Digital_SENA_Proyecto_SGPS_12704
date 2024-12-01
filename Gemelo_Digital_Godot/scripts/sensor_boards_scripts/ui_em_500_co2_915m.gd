#Heredamos de la clase 'Control'
extends Control

#Llamamos al cliente de 'WebSockets'
@onready var WebSocketClient = get_node("../../../WebSocketClient")

#Llamamos al cliente de 'HTTP'
@onready var HTTPClientInitialStatus = get_node("../../../HTTPClient")

#Definimos las salidas de texto
@onready var co2_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer/co2_measure
@onready var temperature_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer2/temperature_measure
@onready var humidity_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer3/humidity_measure
@onready var pressure_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer4/pressure_measure

# Called when the node enters the scene tree for the first time.
func _ready():
	
	#Conectamos las 'signals'
	WebSocketClient.message_from_em_500_co2_915m.connect(_on_received_message)
	HTTPClientInitialStatus.initial_status_em_500_co2_915m.connect(_on_received_message)

#Escuchamos la 'signal'
func _on_received_message(msg):
	
	#Convertimos a JSON
	var message = JSON.parse_string(msg)

	#Mostramos en las cajas de texto
	co2_measure_text_client.text = str(message["CO2"])
	temperature_measure_text_client.text = str(message["temperature"])
	humidity_measure_text_client.text = str(message["humidity"])
	pressure_measure_text_client.text = str(message["ap"])
	
	
