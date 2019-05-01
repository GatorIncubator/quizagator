#!/bin/bash

function get_latest_version() {
    local tag
    tag="$(curl -s -X "GET" "https://api.github.com/repos/gatoreducator/quizagator/tags" | jq -r '.[0].name')"

    if [[ -z "$tag" ]] || [[ "$tag" = "null" ]]; then
        tag="v0.0.0"
    fi

    tag=${tag##v}
    echo "$tag"
    return 0
}

get_latest_version
