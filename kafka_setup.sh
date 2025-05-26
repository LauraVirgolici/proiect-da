# kafka_setup.sh
#!/bin/bash
# Create Kafka topic with multiple partitions
kafka-topics.sh --bootstrap-server kafka:9092 \
  --create --topic transactions \
  --partitions 3 --replication-factor 1