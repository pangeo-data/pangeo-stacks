#!/bin/bash

set -x

echo "printing environment in push script"
env
echo "end printing of environment in push script"

echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin

IMAGE_NAME=${DOCKER_ID}/${IMAGE}:${CALVER}
IMAGE_LATEST=${DOCKER_ID}/${IMAGE}:latest

echo "docker tag ${IMAGE_NAME} ${IMAGE_LATEST}"
docker tag ${IMAGE_NAME} ${IMAGE_LATEST}

docker push ${IMAGE_NAME}
docker push ${IMAGE_LATEST}
