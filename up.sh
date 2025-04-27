#!/bin/bash

ENV_FILE=${1:-.env}
echo "Using env file: $ENV_FILE"

if [ "$(docker ps -q -f name=queuetopia-notif)" ]; then
  echo "Stopping container queuetopia-notif..."
  docker stop queuetopia-notif
fi

if [ "$(docker ps -aq -f name=queuetopia-notif)" ]; then
  echo "Removing container queuetopia-notif..."
  docker rm queuetopia-notif
fi


docker build -t queuetopia-notification .
docker run -d -p 5020:5020 --env-file "$ENV_FILE" --name queuetopia-notif queuetopia-notification

echo "Checking running containers..."
docker ps
