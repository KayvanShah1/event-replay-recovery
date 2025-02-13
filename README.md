# Event Replay Recovery
A tool for recovering and replaying missed events in an event-driven system, ensuring accurate recalculations without relying on traditional databases.

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