import paho.mqtt.client as mqtt
import random
import time


MQTT_BROKER = "localhost"
TOPIC_TEMP = "test/temperature"
TOPIC_HUMIDITY = "test/humidity"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

while True:
    temperature = round(random.uniform(20.0, 35.0), 2)
    humidity = round(random.uniform(30.0, 90.0), 2)
    
    client.publish(TOPIC_TEMP, temperature)
    client.publish(TOPIC_HUMIDITY, humidity)
    
    print(f"Published: {temperature}°C to {TOPIC_TEMP}, {humidity}% to {TOPIC_HUMIDITY}")
    
    time.sleep(5)
