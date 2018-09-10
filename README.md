# pipeline-runner

A light weight pipeline execution engine focused on primitives used by Distil for pre-processing.

## Installation

Prequisites:

1. Python 3.5+ - https://www.python.org/downloads
1. Pipenv - https://github.com/pypa/pipenv

From the project root, download dependencies and activate the environment:

```bash
pipenv install
```

*Note: pipenv is SLOW - you'll have to wait a few minutes for it to run*

This will install a basic set of D3M primitives - those from the `common_primitves` repo, and the NK PCA Features primitive.

To run a test pipeline:

```shell
pipenv shell
cd distil-pipeline-runner
python3 proto_runner.py ../test/create_pca_features.pln file:///home/chris/data/d3m/196_autoMpg/TRAIN/dataset_TRAIN/datasetDoc.json
```

Additional primitives can be installed manually. Example:

```shell
pipenv install -e git+https://github.com/NewKnowledge/pcafeatures-d3m-wrapper.git#egg=PcafeaturesD3MWrapper
```

### Building GRPC/proto files

If there is a desire to build / update source from the proto definitions install GRPC:

```shell
pip3 install grpcio
pip3 install grpcio-tools googleapis-common-protos
pip3 install mypy-protobuf
```

Generate the protobuf files and MyPy type definitions for them:

```shell
python3 -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=./proto --mypy_out=. ./proto/*.proto
```
