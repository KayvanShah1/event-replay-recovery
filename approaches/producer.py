import json
import random
import time
import numpy as np
from kafka import KafkaProducer

KAFKA_BROKER = "localhost:9092"
EVENT_TOPIC = "temperature-events"

# Kafka Producer Setup
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def log_event(event):
    """Logs an event to Kafka"""
    producer.send(EVENT_TOPIC, event)
    print(event)


def generate_sample_events(num_events=50):
    """Generate sensor data for temperature readings"""
    start_timestamp = int(time.time())

    for i in range(num_events):
        time.sleep(1)
        temperature = np.random.normal(52.5, 2)

        # 5% chance of producing an out-of-bound temperature
        if random.random() < 0.05:
            temperature = random.choice([random.uniform(-100, 0), random.uniform(100, 1000)])

        # Determine status based on temperature
        if 50 <= temperature <= 55:
            status = "normal"
        elif 47 <= temperature < 50:
            status = "low"
        elif 55 < temperature <= 58:
            status = "high"
        else:
            status = "error"

        # Simulate missing events by skipping some timestamps
        if random.random() < 0.1:
            print(f"Skipping event at timestamp {start_timestamp + i}")
            continue

        event = {
            "timestamp": start_timestamp + i,
            "event_type": "TEMPERATURE_SENSOR",
            "temperature": temperature,
            "status": status,
        }
        log_event(event)

    print(f"Logged {num_events} sample events.")


if __name__ == "__main__":
    generate_sample_events(30)
