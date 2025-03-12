from flask import Flask, jsonify
import sqlite3
import requests
import json

# Initializing Flask app
app = Flask(__name__)

DB_NAME = "mqtt_sub/sensor_data.db"
DEEPSEEK_URL = "http://localhost:11434/api/chat"
DEEPSEEK_MODEL = "deepseek-r1:8b"

# Function to get the latest sensor data from the database
def get_latest_sensor_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT temp, humidity, timestamp FROM sensor ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()
    conn.close()
    return data

# Function to analyze data with Deepseek
def analyze_with_deepseek(temp, humidity):
    # Construct the message content with temp and humidity
    content = f"The temperature is {temp}°C and the humidity is {humidity}%, what is the weather like today?"

    data = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": content}
        ],
        "stream": False
    }

    headers = {"Content-Type": "application/json"}

    # Send the request to Deepseek
    response = requests.post(DEEPSEEK_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        message = result["message"]["content"]
        cleaned_message = message.replace("<think>", "").replace("</think>", "").strip()
        return cleaned_message
    else:
        print("Error:", response.status_code, response.text)
        return None

# API endpoint to get sensor data and analysis
@app.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    # Fetch the latest sensor data
    data = get_latest_sensor_data()

    if data:
        temp, humidity, timestamp = data
        analysis_result = analyze_with_deepseek(temp, humidity)

        if analysis_result:
            return jsonify({
                "timestamp": timestamp,
                "temperature": temp,
                "humidity": humidity,
                "analysis": analysis_result
            })
        else:
            return jsonify({"error": "Failed to get analysis from Deepseek"}), 500
    else:
        return jsonify({"error": "No data found in the database"}), 404

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True, host="0.0.0.0", port=5000)

