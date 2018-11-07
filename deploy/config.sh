#!/bin/sh

# name and version of docker image that will be created
DOCKER_IMAGE_NAME=distil-pipeline-runner
DOCKER_IMAGE_VERSION=0.1.0

# base dataset location
D3MINPUTDIR=~/data/d3m_data/datasets/seed_datasets_current

# temperary output location
D3MOUTPUTDIR=/home/chris/dev/go_workspace/src/github.com/unchartedsoftware/distil/outputs

# D3M static models directory
STATIC_RESOURCE_PATH=/home/chris/data/d3m_models

# Private GitHub repo key locations
TIMESERIES_LOADER_KEY_LOC=~/keys/deploy_keys/distil-timeseries-loader/distil-timeseries-loader_rsa
MIRANKING_LOADER_KEY_LOC=~/keys/deploy_keys/distil-mi-ranking/distil-mi-ranking_rsa

