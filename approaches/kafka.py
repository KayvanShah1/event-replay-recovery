from kafka import KafkaConsumer, KafkaProducer
import json
import hashlib

KAFKA_BROKER = "localhost:9092"
TOPIC = "events"
ERROR_LOG = "error_log.json"

def hash_event(event):
    """Generate a hash for deduplication"""
    return hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()

def load_errors():
    """Load list of events that were missed or incorrect."""
    with open(ERROR_LOG, "r") as file:
        return set(json.load(file))  # Assume it contains event IDs

def replay_events():
    consumer = KafkaConsumer(TOPIC, bootstrap_servers=KAFKA_BROKER, auto_offset_reset='earliest')
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    missed_events = load_errors()
    processed_hashes = set()

    for message in consumer:
        event = json.loads(message.value)

        if event['id'] in missed_events and hash_event(event) not in processed_hashes:
            # Recalculate the event (business logic here)
            recalculated_event = process_event(event)

            # Ensure idempotency
            processed_hashes.add(hash_event(event))

            # Publish to event bus
            producer.send("reprocessed-events", recalculated_event)
            print(f"Reprocessed event {event['id']}")

def process_event(event):
    """Mock function to reprocess an event"""
    event['reprocessed'] = True  # Modify event with correct calculation
    return event

if __name__ == "__main__":
    replay_events()
