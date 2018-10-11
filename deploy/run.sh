#!/bin/bash

source ./config.sh

docker run \
    --name pipeline-runner \
    --rm \
    -p 50051:50051 \
    --env D3MOUTPUTDIR=$D3MOUTPUTDIR \
    --env D3MINPUTDIR=$D3MINPUTDIR \
    --env STATIC_RESOURCE_PATH=$STATIC_RESOURCE_PATH \
    -v $D3MINPUTDIR:/input \
    -v $D3MOUTPUTDIR:/output \
    -v $STATIC_RESOURCE_PATH:/static_resources \
    docker.uncharted.software/$DOCKER_IMAGE_NAME:latest
