
# Network Programing Project
This project uses API, MQTT, Docker, Cloudflared (DNS), DB, and Deepseek-r1 to implement the project.

## SmartWeather IoT Project
We designed a project that simulates temperature and humidity sensors around the house to gather data and provide it to Deepseek for weather analysis.

You can follow these steps to install the project.




## Installation Docker

### Step 1: Set up Docker to install Ollama for running Deepseek.

Run Ollama Docker container
```bash
  docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

Execute Deepseek-r1 on Ollama container
```bash
  docker exec -it ollama ollama run deepseek-r1:8b
```

### Step 2: Set up Docker to install Mosquitto.

Pull Eclipse Mosquitto Docker image
```bash
  docker pull eclipse-mosquitto
```

Create directories for Mosquitto configuration, data, and logs
```bash
  mkdir -p mosquitto/config mosquitto/data mosquitto/log
```

Create Mosquitto configuration file with listener and anonymous access settings
```bash
  echo "listener 1883\nallow_anonymous true" > mosquitto/config/mosquitto.conf
```

Run Mosquitto Docker container with custom configurations, data, and logs
```bash
  docker run -d --name mosquitto \
  -p 1883:1883 -p 9001:9001 \
  -v $(pwd)/mosquitto/config:/mosquitto/config \
  -v $(pwd)/mosquitto/data:/mosquitto/data \
  -v $(pwd)/mosquitto/log:/mosquitto/log \
  eclipse-mosquitto
```

### Step 3: Set up Docker to install MQTT Publisher.

Build Docker image for MQTT publish
```bash
docker build -t mqtt-publish .
```

Run MQTT publish Docker container on host network
```bash
docker run -d --name mqtt_publish --network host mqtt-publish
```

## Installation Database (SQLite)
Create a file at netpro_project/mqtt_sub/sensor_data.db

### Step 1: Install SQLite3 (if not already installed).
```bash
sudo apt update
sudo apt install sqlite3
```

### Step 2: Create SQLite3 database and table 

Use the following commands to create a database and a table with fields temp and humidity.
```bash
sqlite3 sensor_data.db
```

Once in the SQLite3 shell, use the following SQL command to create the table.
```bash
CREATE TABLE sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temp REAL NOT NULL,
    humidity REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Step 3: Verify that the table was created successfully.

Use this command to view the tables in the database.
```bash
.tables
```

### Step 4: Exit SQLite3.

Once done working with the database, use the following command to exit the SQLite3 shell.
```bash
.exit
```


## Deployment
To deploy this project run

### Step 1: Run MQTT subscriber to receive sensor data and insert into SQLite.

Run the code to receive sensor data from MQTT subscriber and post it into SQLite.
```bash
  python3 mqtt2sqlite3.py
```

### Step 2: Run the Main code.

Run the code to display the output in the terminal.
```bash
  python3 main.py
```

Run the code if you want the result as an API.
```bash
  python3 mainapi.py
```
