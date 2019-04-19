#!/bin/bash

IMAGE_NAME="gatoreducator/quizagator"
TAG=""

NAME="$IMAGE_NAME"
if ! test -z "$TAG"; then
    NAME="$NAME:$TAG"
fi

docker image rm --force "$NAME"

docker build -t "$NAME" .
