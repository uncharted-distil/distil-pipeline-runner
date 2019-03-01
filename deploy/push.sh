#!/bin/bash

source ./config.sh

docker login $DOCKER_REPO

docker push $DOCKER_REPO/$DOCKER_IMAGE_NAME:${DOCKER_IMAGE_VERSION}
docker push $DOCKER_REPO/$DOCKER_IMAGE_NAME:latest

docker logout $DOCKER_REPO
