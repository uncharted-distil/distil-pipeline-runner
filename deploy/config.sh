#!/bin/sh

# name and version of docker image that will be created
DOCKER_IMAGE_NAME=distil-pipeline-runner
DOCKER_IMAGE_VERSION=0.2.1

# base dataset location
D3MINPUTDIR=/data/datasets/seed_datasets_current

# temperary output location
D3MOUTPUTDIR=/data/output

# D3M static models directory
D3MSTATICDIR=/data/static_resources

# D3M datamart directory
DATAMART_PATH=/data/datamart

# address of the docker repo
DOCKER_REPO=docker.uncharted.software
