#!/bin/bash
echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin

docker tag ${IMAGE_NAME} ${IMAGE_LATEST}

docker push $IMAGE_NAME
docker push $IMAGE_LATEST
