#!/bin/sh

# name and version of docker image that will be created
DOCKER_IMAGE_NAME=distil-pipeline-runner
DOCKER_IMAGE_VERSION=0.1.11

# base dataset location
D3MINPUTDIR=/data/datasets/seed_datasets_current

# temperary output location
D3MOUTPUTDIR=/data/output

# D3M static models directory
STATIC_RESOURCE_PATH=/data/static_resources

# Private GitHub repo key locations
SSH_KEY_LOC=/home/ubuntu/keys/distil-timeseries-loader_rsa
