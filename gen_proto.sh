#!/bin/bash

python3 -m grpc_tools.protoc \
    -I./proto/ta3ta2-api \
    -I./proto \
    --python_out=./pipelinerunner \
    --grpc_python_out=./pipelinerunner \
    --mypy_out=./pipelinerunner \
    ./proto/ta3ta2-api/*.proto \
    ./proto/execute.proto

python3 -m grpc_tools.protoc \
    -I./proto/ta3ta2-api \
    --python_out=./proto/ta3ta2-api/ta3ta2_api \
    --grpc_python_out=./proto/ta3ta2-api/ta3ta2_api \
    --mypy_out=./proto/ta3ta2-api/ta3ta2_api \
    ./proto/ta3ta2-api/*.proto
