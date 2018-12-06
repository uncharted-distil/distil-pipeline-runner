#!/bin/bash

source ./config.sh

# builds distil docker image
docker build \
    -f ../Dockerfile.env \
    --tag docker.uncharted.software/$DOCKER_IMAGE_NAME-env:${DOCKER_IMAGE_VERSION} \
    --tag docker.uncharted.software/$DOCKER_IMAGE_NAME-env:latest ..

docker build \
    -f ../Dockerfile.d3m \
    --tag docker.uncharted.software/$DOCKER_IMAGE_NAME-d3m:${DOCKER_IMAGE_VERSION} \
    --tag docker.uncharted.software/$DOCKER_IMAGE_NAME-d3m:latest ..

docker build \
    -f ../Dockerfile \
    --squash \
    --build-arg SSH_KEY="$(cat $SSH_KEY_LOC)" \
    --tag docker.uncharted.software/$DOCKER_IMAGE_NAME:${DOCKER_IMAGE_VERSION} \
    --tag docker.uncharted.software/$DOCKER_IMAGE_NAME:latest ..
