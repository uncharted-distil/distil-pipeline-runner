#!/bin/bash

source ./config.sh

# builds distil docker image
docker build \
    --no-cache \
    --tag docker.uncharted.software/$DOCKER_IMAGE_NAME:${DOCKER_IMAGE_VERSION} \
    --tag docker.uncharted.software/$DOCKER_IMAGE_NAME:latest ..
