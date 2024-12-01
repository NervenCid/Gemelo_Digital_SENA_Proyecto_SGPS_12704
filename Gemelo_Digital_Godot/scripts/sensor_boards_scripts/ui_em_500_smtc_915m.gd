#Heredamos de la clase 'Control'
extends Control

#Llamamos al cliente de 'WebSockets'
@onready var WebSocketClient = get_node("../../../WebSocketClient")

#Llamamos al cliente de 'HTTP'
@onready var HTTPClientInitialStatus = get_node("../../../HTTPClient")

#Definimos las salidas de texto
@onready var conductivity_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer/conductivity_measure
@onready var temperature_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer2/temperature_measure
@onready var soil_moisture_measure_text_client = $PanelContainer/VBoxContainer/HBoxContainer3/soil_moisture_measure

# Called when the node enters the scene tree for the first time.
func _ready():
	
	#Conectamos las 'signals'
	WebSocketClient.message_from_em_500_smtc_915m.connect(_on_received_message)
	HTTPClientInitialStatus.initial_status_em_500_smtc_915m.connect(_on_received_message)

#Escuchamos la 'signal'
func _on_received_message(msg):
	
	#Convertimos a JSON
	var message = JSON.parse_string(msg)

	#Mostramos en las cajas de texto
	conductivity_measure_text_client.text = str(message["conductivity"])
	temperature_measure_text_client.text = str(message["temperature"])
	soil_moisture_measure_text_client.text = str(message["Soil Moisture"])
	
