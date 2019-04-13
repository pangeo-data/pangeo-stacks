#!/bin/bash

set -x

echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin

CALVER="$( date -u '+%Y.%m.%d' )"
IMAGE_NAME=${IMAGE_PREFIX}${IMAGE}:${CALVER}
IMAGE_LATEST=${IMAGE_PREFIX}${IMAGE}:latest

docker tag ${IMAGE_NAME} ${IMAGE_LATEST}

docker push ${IMAGE_NAME}
docker push ${IMAGE_LATEST}
