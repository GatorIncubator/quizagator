#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

IMAGE_NAME="gatoreducator/quizagator"
TAG="dev-$(source $SCRIPT_DIR/version.sh)"

NAME="$IMAGE_NAME"
if ! test -z "$TAG"; then
    NAME="$NAME:$TAG"
fi

docker image rm --force "$NAME"

docker build -t "$NAME" .
