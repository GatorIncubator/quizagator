#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

NAME="quizagator"
DATA_FOLDER="$SCRIPT_DIR/../data"
IMAGE_NAME="gatoreducator/quizagator"
TAG="$(source $SCRIPT_DIR/version.sh)-dev"
IMAGE="$IMAGE_NAME:$TAG"
INNER_PORT="5000"
OUTER_PORT="4201"


docker stop "$NAME"
docker rm "$NAME"

docker run -e "FLASK_SECRET_KEY=dev" -p "${OUTER_PORT}:${INNER_PORT}" \
    --name "$NAME" --mount "type=bind,source=$DATA_FOLDER,target=/data" \
    "$IMAGE"
