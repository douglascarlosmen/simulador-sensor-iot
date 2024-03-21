import random
import time
import json
from paho.mqtt import client as mqtt_client

# Configuração do MQTT
broker = 'localhost'
port = 1883
topic = "sensor/data"

# Gera um ID de cliente único para a sessão MQTT
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # client = mqtt_client.Client(client_id)
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.username_pw_set("teste", "teste")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        # Simulação dos dados do sensor
        data = {
            "sensor_id": random.randint(1, 100),
            "CO2": random.randint(400, 5000),  # em ppm
            "PM2_5": random.uniform(0, 500),   # em µg/m3
            "temperature": random.uniform(-20, 40),  # em °C
            "humidity": random.uniform(0, 100)  # em %
        }
        msg = json.dumps(data)
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        time.sleep(5)

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()
