#!/bin/bash

source ./config.sh

docker login docker.uncharted.software

docker push docker.uncharted.software/$DOCKER_IMAGE_NAME:${DOCKER_IMAGE_VERSION}
docker push docker.uncharted.software/$DOCKER_IMAGE_NAME:latest

docker logout docker.uncharted.software
