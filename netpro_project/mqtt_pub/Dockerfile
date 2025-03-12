# Use Python 3.9 as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the necessary files into the container
COPY sensor2mqtt.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the sensor2mqtt.py script
CMD ["python", "sensor2mqtt.py"]

