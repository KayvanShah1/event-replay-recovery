import json
import heapq
import time
from kafka import KafkaConsumer, KafkaProducer
import numpy as np

KAFKA_BROKER = "localhost:9092"
EVENT_TOPIC = "temperature-events"
REPROCESSED_TOPIC = "reprocessed-events"

# Kafka Consumer Setup
consumer = KafkaConsumer(
    EVENT_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
)

# Kafka Producer Setup for sending reprocessed events
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def process_event(event):
    """Reprocess the event if needed"""
    clipped, event["temperature"] = clip_temperature(event["temperature"])
    if clipped:
        event["status"] = "corrected"

    producer.send(REPROCESSED_TOPIC, event)  # Send corrected events to Kafka
    print(event)


def replay_events(from_timestamp):
    """Reprocess events from a given timestamp"""
    print(f"Replaying events from timestamp: {from_timestamp}")
    processed_timestamps = set()
    event_heap = []  # Min-heap for maintaining sorted events

    for message in consumer:
        event = message.value
        timestamp = event.get("timestamp", 0)

        if timestamp >= from_timestamp:
            processed_timestamps.add(timestamp)
            heapq.heappush(event_heap, (timestamp, event))

    # Identify and generate missing events
    if event_heap:
        start_time = event_heap[0][0]  # Earliest timestamp
        end_time = event_heap[-1][0]  # Latest timestamp

        expected_timestamps = set(range(start_time, end_time + 1))
        missing_timestamps = expected_timestamps - processed_timestamps

        for timestamp in sorted(missing_timestamps):
            synthetic_event = generate_missing_event(timestamp)
            heapq.heappush(event_heap, (timestamp, synthetic_event))

    # Process sorted events
    while event_heap:
        _, event = heapq.heappop(event_heap)
        process_event(event)

    print("Replay completed.")


def clip_temperature(temperature):
    """Clip temperature to be within range"""
    if temperature < 0:
        return True, 47
    elif temperature > 100:
        return True, 58
    return False, temperature


def generate_missing_event(timestamp):
    """Generate a synthetic event for missing timestamps"""
    synthetic_event = {
        "timestamp": timestamp,
        "event_type": "TEMPERATURE_SENSOR",
        "temperature": np.random.normal(52.5, 1),
        "status": "synthetic",
    }
    # print(f"Generated missing event: {synthetic_event}")
    producer.send(REPROCESSED_TOPIC, synthetic_event)  # Send synthetic event
    return synthetic_event


if __name__ == "__main__":
    replay_from_seconds = 60
    print(f"\nReplaying events from the last {replay_from_seconds} seconds...")
    replay_events(int(time.time()) - replay_from_seconds)
