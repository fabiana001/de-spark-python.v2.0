#!/usr/bin/env bash

docker build -t python-fake-data .

docker run -it python-fake-data

CONTAINER_ID=$(docker ps -alq)

docker cp "$CONTAINER_ID":/opt/app/generated_data .