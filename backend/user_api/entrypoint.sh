#!/bin/bash
set -e

wait_for_service() {
  local name=$1
  local host=$2
  local port=$3

  echo "Waiting for $name at $host:$port..."
  until nc -z "$host" "$port" >/dev/null 2>&1; do
    sleep 1
  done
  echo "$name is up!"
}

wait_for_service "PostgreSQL" "$POSTGRES_HOST" "$POSTGRES_PORT"
wait_for_service "Redis" "$REDIS_HOST" "$REDIS_PORT"
wait_for_service "Kafka" "$KAFKA_HOST" "$KAFKA_PORT"

python3 /src/main.py run_server