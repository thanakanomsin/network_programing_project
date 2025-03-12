import sqlite3
import paho.mqtt.client as mqtt

DB_NAME = "sensor_data.db"
MQTT_BROKER = "localhost"
TOPIC_TEMP = "test/temperature"
TOPIC_HUMIDITY = "test/humidity"

# Create database and table if not exists
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temp REAL NOT NULL,
            humidity REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Global variables to store latest values
latest_temp = None
latest_humidity = None

# MQTT callback for received messages
def on_message(client, userdata, msg):
    global latest_temp, latest_humidity
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    
    if topic == TOPIC_TEMP:
        latest_temp = float(payload)
    elif topic == TOPIC_HUMIDITY:
        latest_humidity = float(payload)

    if latest_temp is not None and latest_humidity is not None:
        save_to_db(latest_temp, latest_humidity)
        latest_temp, latest_humidity = None, None  # Reset after saving

# Save data to SQLite database
def save_to_db(temp, humidity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor (temp, humidity) VALUES (?, ?)", (temp, humidity))
    conn.commit()
    conn.close()
    print(f"Data saved: Temp={temp}, Humidity={humidity}")

# Set up MQTT client
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER)

# Subscribe to topics
client.subscribe(TOPIC_TEMP)
client.subscribe(TOPIC_HUMIDITY)

# Initialize database
init_db()

# Start MQTT loop
print("Listening for MQTT messages...")
client.loop_forever()

