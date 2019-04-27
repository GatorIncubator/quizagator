#!/bin/bash

NAME="quizagator"
IMAGE_NAME="gatoreducator/quizagator"
TAG="dev-$(source ${BASH_SOURCE[0]}/version.sh)"
IMAGE="$IMAGE_NAME:$TAG"
INNER_PORT="5000"
OUTER_PORT="4201"


docker stop "$NAME"
docker rm "$NAME"

docker run -d --name "$NAME" -p "${OUTER_PORT}:${INNER_PORT}" "$IMAGE"
