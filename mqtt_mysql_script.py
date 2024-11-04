# Script Python para conectar al broker y la base de datos

import mysql.connector
import paho.mqtt.client as mqtt

# Configuración de la conexión a MySQL
db = mysql.connector.connect(
    host="localhost", # Cambiar por la IP o dominio del servidor MySQL si no está en localhost
    user="Mariano", # Cambiar por el usuario de MySQL
    password="", # Cambiar por la contraseña de MySQL
    database="sensor_data" # Base de datos donde se guardarán los datos
)
# Cursor para ejecutar comandos SQL
cursor = db.cursor()

# Función para insertar datos en la base de datos
def insertar_datos(temperatura, humedad):
    sql = "INSERT INTO dht22_data (temperatura, humedad) VALUES (%s, %s)"
    val = (temperatura, humedad)
    cursor.execute(sql, val)
    db.commit()
    print(f"Datos guardados: Temperatura={temperatura}°C, Humedad={humedad}%")

# Funciones para manejar los eventos MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT")
        # Suscribirse a los tópicos de temperatura y humedad
        client.subscribe("Temperatura")
        client.subscribe("Humedad")
    else: 
        print(f"Fallo en la conexión al broker. Código de error: {rc}")

# Variables globales para almacenar los valores recibidos
temperatura = None
humedad = None

# Función que se ejecuta al recibir un mensaje
def on_message(client, userdata, msg):
    global temperatura, humedad
    if msg.topic == "Temperatura":
        temperatura = float(msg.payload.decode())
        print(f"Temperatura recibida: {temperatura}°C")
    elif msg.topic == "Humedad":
        humedad = float(msg.payload.decode())
        print(f"Humedad recibida: {humedad}%")
    # Cuando ambos valores estén disponibles, insertar en la base de datos
    if temperatura is not None and humedad is not None:
        insertar_datos(temperatura, humedad)
        # Resetear los valores después de insertarlos
        temperatura = None
        humedad = None

# Configuración del broker MQTT
broker_address = "broker.hivemq.com" # Broker público de HiveMQ
broker_port = 1883 # Puerto para conexión sin TLS

# Inicializar el cliente MQTT
client = mqtt.Client("PythonClient")
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker MQTT
client.connect(broker_address, broker_port)

# Iniciar el bucle de MQTT para escuchar los mensajes
client.loop_forever()