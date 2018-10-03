#!/bin/bash

source ./config.sh

docker run \
    -p 50051:50051 \
    --env D3MOUTPUTDIR=$D3MOUTPUTDIR \
    --env STATIC_RESOURCE_PATH=$STATIC_RESOURCE_PATH \
    -v /input:/input \
    -v $D3MOUTPUTDIR:$D3MOUTPUTDIR \
    -v $STATIC_RESOURCE_PATH:$STATIC_RESOURCE_PATH \
     docker.uncharted.software/$DOCKER_IMAGE_NAME:latest
