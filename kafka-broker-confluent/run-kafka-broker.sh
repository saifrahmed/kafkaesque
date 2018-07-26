#!/bin/bash

# MUST READ: https://docs.confluent.io/current/installation/docker/docs/quickstart.html#getting-started-with-docker-client

docker network create confluent
docker run -d \
    --net=confluent \
    --name=kafka \
    -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
    -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 \
    -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    -p 9092:9092 \
    confluentinc/cp-kafka:4.1.0

docker run \
  --net=confluent \
  --rm confluentinc/cp-kafka:4.1.0 \
  kafka-topics --create --topic prices --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181

docker run \
  --net=confluent \
  --rm \
  confluentinc/cp-kafka:4.1.0 \
  kafka-topics --describe --topic prices --zookeeper zookeeper:2181
