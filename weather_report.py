import requests
import pika
import json
import time
import os
from datetime import datetime

# API
API_KEY = '737a4351018d70512bde56f27943000c'
CITY_NAME = 'Jerusalem'
API_URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&units=metric'

# RabbitMQ
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
QUEUE_NAME = 'weather_data'

# Sampling rate, use 10 sec for debug
SAMPLING_RATE = 10

def get_weather():
    print("Fetching weather data...") # debug
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()

    # Timestamp with ms
    timestamp = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'

    weather_info = {
        'timestamp': timestamp,
        'city': CITY_NAME,
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'weather': data['weather'][0]['description']
    }

    return weather_info

def send_to_rabbitmq(message):
    print("Connecting to RabbitMQ...") # debug
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2  # שמירה על הודעה גם לאחר קריסה
        )
    )
    print("Message sent successfully.") # debug
    connection.close()

def main():
    print("Weather script started...") # debug
    while True:
        try:
            weather_data = get_weather()
            print(f"Sending data: {weather_data}") # debug
            send_to_rabbitmq(weather_data)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(SAMPLING_RATE)

if __name__ == '__main__':
    main()
