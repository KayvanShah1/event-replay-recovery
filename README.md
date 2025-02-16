# Event Replay Recovery
A tool for recovering and replaying missed events in an event-driven system, ensuring accurate recalculations without relying on traditional databases.

## Scenario: Monitoring Temperature of Equipment Using Sensors
- **Context**: Monitoring industrial machinery using temperature sensors that emit timestamped events, including temperature readings and status (normal or deviated).
  
- **Problem**: Errors like missing, corrupted, or out-of-range events can affect data accuracy, crucial for maintaining safe machinery operation. Events may also be missed due to network issues or processing failures.

- **Goal**: Aggregate and process temperature data, reprocess missing or erroneous events, and generate synthetic data for gaps to ensure complete, accurate time series for analysis.

- **Assumptions Made:**
    1. **Data Integrity**: Events include timestamps, necessary for sequencing and identifying missing data.
    2. **Out-of-Range Values**: Valid temperature range is 50–55°C; any values outside this range are erroneous.
    3. **Error Rates**: ~5% of data may be out-of-range, and 10% may be missing (simulated).
    4. **Event Structure**: Each event includes a timestamp, temperature reading, and status.

## Approach Explaination
I implemented a file-based solution using `JSONL (JSON lines)` for storing events and a `heap` data structure to ensure that events are processed in the correct order. The solution involves the following key components:

1. **Event Logging**: Events are logged to a file in `JSONL` format. This approach allows for efficient storage and retrieval of events.

2. **Heap-Based Event Ordering**: A `min-heap` is used to maintain events in chronological order based on their timestamps. This ensures that events are replayed in the correct sequence.

3. **StringIO Buffer for Replay**: A `StringIO` buffer is utilized to store processed events temporarily before they are outputted. This facilitates efficient handling of event replay.

### Implementation Details
The implementation includes the following functionalities:

1. **Event Generation**: A configurable event generator with adjustable error and skip rates. It generates sample events with timestamps and temperature readings, intentionally skipping some events to simulate missing data

2. **Event Replay**: The system replays events from a specified timestamp, ensuring that all events, including missing ones, are processed correctly.

3. **Data Consistency**: Basic data validation is performed to ensure temperature readings are within a valid range.

#### Accuracy and Consistency in the recalculated results
- Ensure consistency by checking for already reprocessed events via a reprocessed set, which prevents unnecessary duplicate recalculations.
- For missing events - generate synthetic events based on probabilistic assumptions (temperature distributions), ensuring they are logically consistent with the system's behavior.

#### Data Transmission Medium
- For simplicity I choose JSON format - readability and self-descriptive fields, flexible schema
- Alternatively, we can CSV format - raw data transmission, compact, max speed and min size
- Alternatively, for structured data transmission Protobuf/Avro or any row based format can be used.

## Discussion
### Trade-offs and Limitations
- **Scalability**: The file-based approach has scalability limitations compared to distributed systems like Kafka. However, it is suitable for smaller-scale applications or prototyping.

- **Performance**: Using a heap for ordering events is efficient for small to medium-sized datasets but may not be optimal for very large datasets.

### Approach with Additional Tools
- **Distributed Event Stores**: Implementing a distributed event store like Kafka would significantly enhance scalability and reliability.

- **Dead Letter Queues (DLQs)**: Incorporating DLQs would improve error handling by capturing and reprocessing failed events.

- **Database/Data warehouse**: Store historical events data for efficient batch processing and analysis. Can handle large amounts of data and addresses issues with advanced processing techniques like imputation, interpolation and incorporate complex and better valition methodologies. (Better than on-the-fly recalculations annd corrections)

- **Cloud-based self managed services**: Can reduce the overhead of maintainance of clusters and scale automatically depending upon usage and demand. Can incur significant costs though.

- **Parallel Processing**: Use parallel processing techniques or frameworks like Apache Spark to process events concurrently.

## Alternative Approaches:
| Approach                  | Best for                                      | Retention | Scalability | Complexity |
|---------------------------|-----------------------------------------------|-----------|-------------|------------|
| **Kafka/Event Bus**        | Large-scale, distributed event processing     | Long-term  | High        | Medium     |
| **Redis + Heap**           | Low-latency replay for short-term events      | Short-term | Medium      | Low        |
| **Cloud Queues (SNS/SQS, Pub/Sub)** | Serverless, cloud-native event replays       | Configurable | High        | Low        |
| **Event Sourcing (EventStoreDB)** | Full event history replay                  | Long-term  | Medium-High | High       |
| **Log-based Replay (Flink, CDC)** | Streaming systems & large event reprocessing | Long-term  | High        | Medium     |
| **File-based Replay (S3, HDFS)** | Batch processing & historical event recovery | Long-term  | Medium      | Low        |
| **Memory-based Replay (Ring Buffers)** | Real-time low-latency recovery            | Short-term | Low         | Low        |
| **File-based (JSON, CSV, Parquet)** | Simple event logging                       | Yes        | Medium      | Easy       |
| **In-memory queue (Heap, `deque`)** | Fast event replay                           | No         | Medium      | Easy       |
| **Pickle-based storage**     | Simple persistent storage                    | Yes        | Medium      | Easy       |
| **Redis Streams**           | Real-time event processing with persistence   | Long-term  | High        | Medium     |

### Choosing One Over Another

- **Choose Kafka/Event Bus** for large-scale distributed systems where high scalability and long-term retention are crucial, need fine grained control over resources.
- **Prefer Redis Streams** for real-time processing and long-term data retention.
- **Opt for Cloud Queues** in serverless architectures for ease of use, automatic scalability
- **Select File-based Approaches** for simple logging or batch processing scenarios where real-time capabilities are a priority, small scale systems.

## Setup Steps
**1. Create Conda Environment:**

Run the following command to create a new conda environment named `kafka`:

```bash
conda create --name event_streaming python=3.12
```

Activate the environment:

```bash
conda activate event_streaming
```
**2. Install Dependencies:**

Run this command to install it in your conda environment:

```bash
pip install -r requirements.txt
```

### Acknowledgement & Learning Experience
This assignment was a valuable learning experience, allowing me to explore concepts around data streaming and processing. Over the course of a week, I dedicated time to understanding these concepts and practicing related problems on platforms like LeetCode. The change of pace from typical coding challenges was refreshing, and I enjoyed the opportunity to apply theoretical knowledge to a practical problem.

#### LICENSE
This repository is licensed under the `MIT` License. See the [LICENSE](LICENSE) file for details.

#### Disclaimer

<sub>
The content and code provided in this repository are for educational and demonstrative purposes only. The project may contain experimental features, and the code might not be optimized for production environments. The authors and contributors are not liable for any misuse, damages, or risks associated with this code's direct or indirect use. Users are strictly advised to review, test, and completely modify the code to suit their specific use cases and requirements. By using any part of this project, you agree to these terms.
</sub>