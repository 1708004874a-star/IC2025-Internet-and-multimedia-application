import json
import paho.mqtt.client as mqtt
from .models import SensorData

ID="HSC02" # Sensor ID
MQTT_BROKER = "ia.ic.polyu.edu.hk"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/sensor-B06"
MQTT_QOS = 1

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        node_id = payload.get("node_id")
        loc = payload.get("loc")
        temp = payload.get("temp")
        hum = payload.get("hum")
        light = payload.get("light")
        snd = payload.get("snd")

        
        SensorData.objects.create(
            node_id=node_id,
            loc=loc,
            temp=temp,
            hum=hum,
            light=light,
            snd=snd,
        )
        print(f"Data stored: {payload}")
    except Exception as e:
        print(f"Error processing message: {e}")

client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)

client.subscribe(MQTT_TOPIC, MQTT_QOS)

client.loop_start()