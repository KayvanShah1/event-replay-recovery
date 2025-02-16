import heapq
import json
import os
import random
import time
from io import StringIO

import numpy as np

logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(logs_dir, exist_ok=True)

EVENT_LOG_FILE = os.path.join(logs_dir, "file_based_json_events_log.jsonl")
REPROCESSED_EVENTS_FILE = os.path.join(logs_dir, "reprocessed_events.jsonl")


# Function to log events
def log_event(event):
    """Logs an event to the event log file"""
    with open(EVENT_LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")


# Function to replay events from a timestamp
def replay_events(from_timestamp):
    """Reprocess events from a given timestamp"""
    if not os.path.exists(EVENT_LOG_FILE):
        print("No log file found. No events to replay.")
        return

    processed_timestamps = set()
    event_heap = []  # Min-heap to maintain sorted events
    buffer = StringIO()

    with open(EVENT_LOG_FILE, "r") as f:
        for line in f:
            event = json.loads(line)
            timestamp = event.get("timestamp", 0)
            if timestamp >= from_timestamp:
                # process_event(event)
                processed_timestamps.add(timestamp)
                heapq.heappush(event_heap, (timestamp, event))

    # Identify and generate missing events
    if event_heap:
        start_time = event_heap[0][0]  # Earliest timestamp
        end_time = event_heap[-1][0]  # Latest timestamp

        expected_timestamps = set(range(start_time, end_time + 1))
        missing_timestamps = expected_timestamps - processed_timestamps

        # Generate and store synthetic events for missing timestamps
        for timestamp in sorted(missing_timestamps):
            synthetic_event = generate_missing_event(timestamp)
            heapq.heappush(event_heap, (timestamp, synthetic_event))

    # Write ordered events into the in-memory buffery
    while event_heap:
        _, event = heapq.heappop(event_heap)
        event = process_event(event)
        buffer.write(json.dumps(event) + "\n")

    # Reset buffer cursor before reading
    buffer.seek(0)
    for line in buffer:
        event = json.loads(line)
        print(event)
    buffer.close()

    print("Replay completed.")


def process_event(event):
    """Reprocess event only if it hasn’t been reprocessed before"""
    reprocessed_set = get_reprocessed_events()

    # Skip if event has been reprocessed before
    if event["timestamp"] in reprocessed_set:
        return event

    rep, event["temperature"] = clip_temperature(event["temperature"])

    if rep:
        event["status"] = "corrected"

    with open(REPROCESSED_EVENTS_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

    return event


def get_reprocessed_events():
    """Load previously reprocessed event timestamps"""
    if not os.path.exists(REPROCESSED_EVENTS_FILE):
        return set()

    with open(REPROCESSED_EVENTS_FILE, "r") as f:
        return {json.loads(line)["timestamp"] for line in f}


def clip_temperature(temperature):
    """Clip the temperature to be within the valid range [50, 55]"""
    if temperature < 0:
        return True, 47
    elif temperature > 100:
        return True, 58
    return False, temperature


def generate_missing_event(timestamp):
    """Generate a synthetic event to fill the missing gap"""
    synthetic_event = {
        "timestamp": timestamp,
        "event_type": "TEMPERATURE_SENSOR",
        "temperature": np.random.normal(52.5, 1),
        "status": "normal",
        "synthetic": True,
    }
    log_event(synthetic_event)
    return synthetic_event


def generate_sample_events(num_events=50):
    """Generate sensor data for temperature readings"""
    start_timestamp = int(time.time())
    events = []
    for i in range(num_events):
        # temperature = random.uniform(50, 55)
        temperature = np.random.normal(52.5, 2)

        # 5% chance of producing an out-of-bound temperature
        if random.random() < 0.05:  # 5% chance
            temperature = random.choice([random.uniform(-100, 0), random.uniform(100, 1000)])  # Out of range values

        if 50 <= temperature <= 55:
            status = "normal"
        elif 47 <= temperature < 50:
            status = "low"
        elif 55 < temperature <= 58:
            status = "high"
        else:
            status = "error"

        # Simulate missing events by randomly skipping some timestamps
        if random.random() < 0.1:
            print(f"Skipping event at timestamp {start_timestamp + i}")
            continue

        event = {
            "timestamp": start_timestamp + i,
            "event_type": "TEMPERATURE_SENSOR",
            "temperature": temperature,
            "status": status,
        }
        events.append(event)
        log_event(event)
        print(event)
        time.sleep(1)

    print(f"Logged {len(events)} sample events.")


if __name__ == "__main__":
    generate_sample_events(30)

    replay_from_seconds = 60
    print(f"\n Replaying events from the last {replay_from_seconds} seconds...")
    replay_events(int(time.time()) - replay_from_seconds)
