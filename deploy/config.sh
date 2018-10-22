#!/bin/sh

# name and version of docker image that will be created
DOCKER_IMAGE_NAME=distil-pipeline-runner
DOCKER_IMAGE_VERSION=0.1.0

# base dataset location
D3MINPUTDIR=/input

# temperary output location
D3MOUTPUTDIR=/output

# D3M static models directory
STATIC_RESOURCE_PATH=/static_resources

# Time series loader SSH deploy key location
SSH_KEY_LOCATION=~/keys/distil-timeseries-loader_rsa

