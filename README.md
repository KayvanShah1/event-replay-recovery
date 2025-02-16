# Event Replay Recovery
A tool for recovering and replaying missed events in an event-driven system, ensuring accurate recalculations without relying on traditional databases.

## Scenario: Monitoring Temperature of Equipment Using Sensors
- **Context**: Monitoring industrial machinery using temperature sensors that emit timestamped events, including temperature readings and status (normal or deviated).
  
- **Problem**: Errors like missing, corrupted, or out-of-range events can affect data accuracy, crucial for maintaining safe machinery operation. Events may also be missed due to network issues or processing failures.

- **Goal**: Aggregate and process temperature data, reprocess missing or erroneous events, and generate synthetic data for gaps to ensure complete, accurate time series for analysis.

> ### Assumptions Made:
> 1. **Data Integrity**: Events include timestamps, necessary for sequencing and identifying missing data.
> 2. **Out-of-Range Values**: Valid temperature range is 50–55°C; any values outside this range are erroneous.
> 3. **Error Rates**: ~5% of data may be out-of-range, and 10% may be missing (simulated).


## Setup Steps
**1. Create Conda Environment:**

Run the following command to create a new conda environment named `kafka`:

```bash
conda create --name kafka python=3.12
```

Activate the environment:

```bash
conda activate kafka
```
**2. Install Dependencies:**

Run this command to install it in your conda environment:

```bash
pip install -r requirements.txt
```

## References
1. [Apache Kafka - KRaft Mode: Setup](https://dev.to/deeshath/apache-kafka-kraft-mode-setup-5nj)
2. [Kafka Cluster with Docker Compose](https://medium.com/@erkndmrl/kafka-cluster-with-docker-compose-5864d50f677e)