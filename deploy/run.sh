#!/bin/bash

source ./config.sh

docker run \
    -p 50051:50051 \
    -v /usr/local/d3m/datasets:/usr/local/d3m/datasets \
    -v /usr/local/d3m/output:/usr/local/d3m/output \
    -v /usr/local/d3m/static_resources:/usr/local/d3m/static_resources \
     docker.uncharted.software/$DOCKER_IMAGE_NAME:latest
