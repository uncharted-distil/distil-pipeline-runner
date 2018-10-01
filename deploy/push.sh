#!/bin/bash

source ./config.sh

docker push docker.uncharted.software/$DOCKER_IMAGE_NAME:${DOCKER_IMAGE_VERSION}
docker push docker.uncharted.software/$DOCKER_IMAGE_NAME:latest
