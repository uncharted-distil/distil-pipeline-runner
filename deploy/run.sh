#!/bin/bash

source ./config.sh

# add VERBOSE_PRIMTIIVE_OUTPUT=1 to env vars below to enable primitive param / result
# output

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
    -v $DATAMART_PATH:$DATAMART_PATH \
    docker.uncharted.software/$DOCKER_IMAGE_NAME:latest
