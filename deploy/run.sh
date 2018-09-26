#!/bin/bash

source ./config.sh

docker run -p 50051:50051 docker.uncharted.software/$DOCKER_IMAGE_NAME:latest
