# encoding=utf8

"""
Incluyendo estos arrobas luego un programa puede leerlos automaticamente y generar código
@author = Lander Lejarza y Diego González
@año = Año 2019/02
@proyecto = Registro de temp. y Humedad con Raspberry Pi
@desc = este programa lee los datos del sensor y  los sube a Thingspeak utilizando el protocolo mqtt
https://pypi.org/project/paho-mqtt/#constructor-reinitialise
"""

########## LIBRERÍAS ##########
import paho.mqtt.publish as publish #al poner as publish, no tenemos que poner paho.mqtt.publish continuamente
import httplib # para la conexión TCP (https://docs.python.org/2/library/httplib.html)
import urllib # https://docs.python.org/2/library/urllib.html
import json # https://www.w3schools.com/python/python_json.asp
import Adafruit_DHT # lhttps://github.com/adafruit/Adafruit_Python_DHT
import time
# NO SE USA ESTA LIBRERIA: pip install RPi.GPIO en la terminal de la raspberry pi
# import RPi.GPIO as IO


# A MODIFICAR POR CADA USUARIO SEGÚN SU CUENTA
USER_API_KEY = '0W19SHCTIJK8MS0Y' # Para borrar o crear un canal (https://thingspeak.com/account/profile)


########## SENSOR DHT22 ##########
# Definimos qué sensor vamos a usar, hay diferentes dentro de la librería
sensor = Adafruit_DHT.DHT22
# Definimos el pin lógico de la raspberry pi(no físico) al que hemos conectado el sensor
# La distribución: https://gpiozero.readthedocs.io/en/stable/recipes.html
pin = 22


########## CREACIÓN DE LOS DOS CANALES ##########
# Conectarse a thingspeak mediante TCP
server = 'api.thingspeak.com'
connTCP = httplib.HTTPSConnection(server) #Creamos la conexión TCP
print("Estableciendo conexión TCP..."), #la coma es para seguir los prints en la misma línea
connTCP.connect() # Nos conectamos
print("Conexión TCP establecida!")

# Creamos la petición http (https://es.mathworks.com/help/thingspeak/createchannel.html)
print ("Creando canales...")
method = "POST"
relative_uri = "/channels.json"  # Para que devuelva en formato json: {"field1":"5"}
# Con llaves,{}, se crea un diccionario: secuencia desordenada de pares, {nombre : valor}
headers1 = {'Host': server, 'Content-Type': 'application/x-www-form-urlencoded'} # Se suben en formato formulario: field1=5&field2=10
headers2 = {'Host': server, 'Content-Type': 'application/x-www-form-urlencoded'} # Se suben en formato formulario: field1=5&field2=10
# Para los dos canales
payload1 = {'api_key': USER_API_KEY, 'name': 'Canal 1 <Diego>', 'field1': 'Temperatura', 'field2': 'Humedad'}
payload2 = {'api_key': USER_API_KEY, 'name': 'Canal 2 <Lander>', 'field1': 'Temperatura', 'field2': 'Humedad'}
payload_encoded1 = urllib.urlencode(payload1) # Se codifica el payload: se pasa de formato diccionario a formato fomulario
payload_encoded2 = urllib.urlencode(payload2) # Se codifica el payload: se pasa de formato diccionario a formato fomulario
headers1['Content-Length'] = len(payload_encoded1)  # Añadimos al diccionario la longitud del payload
headers2['Content-Length'] = len(payload_encoded2)  # Añadimos al diccionario la longitud del payload

# Lanzamos la petición del canal 1
print("Enviar petición 1 HTTP..."),
connTCP.request(method, relative_uri, body=payload_encoded1, headers=headers1)
print("Petición 1 enviada!")
print("Esperando respuesta HTTP...")
respuesta = connTCP.getresponse()
status = respuesta.status
print ("\tStatus 1: " + str(status))
print ("Canal 1 creado!")
contenido = respuesta.read()  # Devuelve una cadena de texto en formato json
# Hay que decodificarlo, pasándolo de formato json a formato diccionario (uso de la librería json)
contenido_json = json.loads(contenido)
CHANNEL_ID_1 = contenido_json['id']
WRITE_API_KEY_1 = contenido_json['api_keys'][0]['api_key'] #


# Lanzamos la petición del canal 2
print("Enviar petición 2 HTTP..."),
connTCP.request(method, relative_uri, body=payload_encoded2, headers=headers2)
print("Petición 2 enviada!")
print("Esperando respuesta HTTP...")
respuesta = connTCP.getresponse()
status = respuesta.status
print ("\tStatus 2: " + str(status))
print ("Canal 2 creado!")
contenido = respuesta.read()  # Devuelve una cadena de texto en formato json
# Hay que decodificarlo, pasándolo de formato json a formato diccionario (uso de la librería json)
contenido_json = json.loads(contenido)
CHANNEL_ID_2 = contenido_json['id']
WRITE_API_KEY_2 = contenido_json['api_keys'][0]['api_key'] #



 
########## PROTOCOLO MQTT PARA LOS DOS CANALES ##########
# https://es.mathworks.com/help/thingspeak/subscribetoachannelfeed.html
broker = "mqtt.thingspeak.com"
# https://es.mathworks.com/help/thingspeak/publishtoachannelfeed.html
# En el topic hay partes fijas y parametrizadas. Parametrizadas: <channelID> y <apikey>
topiko = "channels/<channelID>/publish/<apikey>"
# en https://thingspeak.com/channels/680585/api_keys
topiko1 = "channels/" + str(CHANNEL_ID_1) + "/publish/" + str(WRITE_API_KEY_1)
topiko2 = "channels/" + str(CHANNEL_ID_2) + "/publish/" + str(WRITE_API_KEY_2)


flag = 1 #Valor que oscilará entre 1 y -1
#Humedad = 0
#Temperatura = 0
########## LECTURA DE LOS SENSORES ##########
while(True):
    # Empezamos a medir el tiempo de los 10 segundos
    start = time.time() #Medimos el tiempo de inicio de las mediciones
    Humedad, Temperatura = Adafruit_DHT.read_retry(sensor, pin)

    #time.sleep(3)
    #Temperatura = Temperatura + 2
    #Humedad = Humedad + 1

    print('Temp.={0:0.1f}ºC  Humedad={1:0.1f}%'.format(Temperatura, Humedad)) #Display en la pantalla para saber que lee
    carga = "field1=" + str(Temperatura) + "&field2=" + str(Humedad) # Preparamos el payload del mensaje

    # Subir datos al primer canal
    elapsed = time.time() #Medimos el tiempo final de las mediciones
    if (elapsed - start) < 10:
    	time.sleep(10 - (elapsed - start)) #Compensamos el tiempo que tarda el sensor en realizar las mediciones
    if flag == 1:
        # https://es.mathworks.com/help/thingspeak/publishtoachannelfeed.html

        #Publish a single message to a broker, then disconnect cleanly.
        #Hay que definir a dónde se manda el mensaje (maquina/broker = hostname, y topic) y qué mensaje se manda (payload)
        publish.single(topiko1, payload=carga, hostname=broker)
        print ("Datos subidos al canal 1.")

    # Subir datos al segundo canal
    else:
        # https://es.mathworks.com/help/thingspeak/publishtoachannelfeed.html
        carga = "field1=" + str(Temperatura) + "&field2=" + str(Humedad)

        #Publish a single message to a broker, then disconnect cleanly.
        #Hay que definir a dónde se manda el mensaje (maquina/broker = hostname, y topic) y qué mensaje se manda (payload)
        publish.single(topiko2, payload=carga, hostname=broker)
        print ("Datos subidos al canal 2.")

    
    flag = -flag#Toggle del valor

























