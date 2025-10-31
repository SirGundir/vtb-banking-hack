#!/bin/sh
set -e

echo "Waiting for Postgres..."
until nc -z vtb_banking.postgres 5432; do
  sleep 1
done

echo "Waiting for Redis..."
until nc -z vtb_banking.redis 6379; do
  sleep 1
done

echo "Starting app..."
python main.py