#!/bin/bash

source ./config.sh

docker run \
    --name pipeline-runner \
    --rm \
    -d \
    -p 50051:50051 \
    --env D3MOUTPUTDIR=$D3MOUTPUTDIR \
    --env D3MINPUTDIR=$D3MINPUTDIR \
    --env STATIC_RESOURCE_PATH=$STATIC_RESOURCE_PATH \
    -v $D3MINPUTDIR:$D3MINPUTDIR \
    -v $D3MOUTPUTDIR:$D3MOUTPUTDIR \
    -v $STATIC_RESOURCE_PATH:$STATIC_RESOURCE_PATH \
    docker.uncharted.software/$DOCKER_IMAGE_NAME:latest
