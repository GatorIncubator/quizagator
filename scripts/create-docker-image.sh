#!/bin/bash

IMAGE_NAME="gatoreducator/quizagator"
TAG="dev-$(source ${BASH_SOURCE[0]}/version.sh)"

NAME="$IMAGE_NAME"
if ! test -z "$TAG"; then
    NAME="$NAME:$TAG"
fi

docker image rm --force "$NAME"

docker build -t "$NAME" .
