#!/bin/bash

NAME="quizagator"
IMAGE="gatoreducator/quizagator:latest"
INNER_PORT="3301"
OUTER_PORT="4201"


docker stop "$NAME"
docker rm "$NAME"

docker run -d --name "$NAME" -p "${OUTER_PORT}:${INNER_PORT}" "$IMAGE"
