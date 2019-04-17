#!/bin/bash
set -euxo pipefail

echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin

IMAGE=${1}

CALVER="$( date -u '+%Y.%m.%d' )"
IMAGE_NAME=${IMAGE_PREFIX}${IMAGE}:${CALVER}
IMAGE_LATEST=${IMAGE_PREFIX}${IMAGE}:latest

docker tag ${IMAGE_NAME} ${IMAGE_LATEST}

docker push ${IMAGE_NAME}
docker push ${IMAGE_LATEST}


ONBUILD_IMAGE_NAME=${IMAGE_PREFIX}${IMAGE}-onbuild:${CALVER}
ONBUILD_IMAGE_LATEST=${IMAGE_PREFIX}${IMAGE}-onbuild:latest

docker tag ${ONBUILD_IMAGE_NAME} ${ONBUILD_IMAGE_LATEST}

docker push ${ONBUILD_IMAGE_NAME}
docker push ${ONBUILD_IMAGE_LATEST}
