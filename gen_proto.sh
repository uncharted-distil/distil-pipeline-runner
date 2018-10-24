#!/bin/bash

python3 -m grpc_tools.protoc \
    -I./proto/ta3ta2-api \
    -I./proto \
    --python_out=./pipelinerunner \
    --grpc_python_out=./pipelinerunner \
    --mypy_out=./pipelinerunner \
    ./proto/ta3ta2-api/value.proto \
    ./proto/ta3ta2-api/primitive.proto \
    ./proto/ta3ta2-api/pipeline.proto \
    ./proto/execute.proto