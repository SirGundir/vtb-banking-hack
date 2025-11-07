#!/bin/bash

# Пример топиков
TOPICS=("download_user_account" "download_user_transaction" "download_user_account")
PARTITIONS=3
REPLICATION=1

for TOPIC in "${TOPICS[@]}"; do
    kafka-topics.sh \
        --bootstrap-server localhost:9092 \
        --create \
        --if-not-exists \
        --topic "$TOPIC" \
        --partitions $PARTITIONS \
        --replication-factor $REPLICATION
done
