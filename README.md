# pipeline-runner

A light weight pipeline execution engine focused on primitives used by Distil for pre-processing.

## Installation

### Prerequisites
1. Python 3.5+
1. Pip version 9.0.1+

Add d3m standard library:
```
pip3 install d3m
```

To enable linting with 3.5 typing support install Mypy:

```
pip3 install mypy
```

* Note - will migrate to pipenv and add a setup.py, so above is a temporary step

### Building GRPC/proto files

If there is a desire to build / update source from the proto definitions install GRPC:

```bash
pip3 install grpcio
pip3 install grpcio-tools googleapis-common-protos
pip3 install mypy-protobuf
```

Generate the protobuf files and MyPy type definitions for them:

```bash
python3 -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=./proto --mypy_out=. ./proto/*.proto
```
