#!/bin/bash
set -e

wait_for_postgres() {
  echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
  until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" >/dev/null 2>&1; do
    sleep 1
  done
  echo "PostgreSQL is up!"
}

wait_for_redis() {
  echo "Waiting for Redis at $REDIS_HOST:$REDIS_PORT..."
  until redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping >/dev/null 2>&1; do
    sleep 1
  done
  echo "Redis is up!"
}

wait_for_kafka() {
  echo "Waiting for Kafka at $KAFKA_HOST:$KAFKA_PORT..."
  # просто TCP + доп. задержка
  until nc -z "$KAFKA_HOST" "$KAFKA_PORT" >/dev/null 2>&1; do
    sleep 1
  done
  echo "Kafka TCP port is open, waiting extra 10s..."
  sleep 10
}

wait_for_postgres
wait_for_redis
wait_for_kafka

python3 /src/main.py run_server
