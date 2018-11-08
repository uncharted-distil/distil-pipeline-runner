#!/bin/sh

# name and version of docker image that will be created
DOCKER_IMAGE_NAME=distil-pipeline-runner
DOCKER_IMAGE_VERSION=0.1.0

# base dataset location
D3MINPUTDIR=~/data/d3m_data/datasets/seed_datasets_current

# temperary output location
D3MOUTPUTDIR=~/dev/go_workspace/src/github.com/unchartedsoftware/distil/outputs

# D3M static models directory
STATIC_RESOURCE_PATH=~/data/d3m_models

# Private GitHub repo key locations
SSH_KEY_LOC=~/keys/d3mbuild/distil-pipeline-runner-build/distil-pipeline-runner-build_rsa

