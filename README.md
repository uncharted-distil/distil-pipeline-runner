# pipeline-runner

A light weight pipeline execution engine focused on primitives used by Distil for pre-processing.

## Installation

Install python

```bash
sudo apt install build-essential libssl-dev libffi-dev python3-dev python3-pip python3-venv
```

Setup and activate virtual environment:

```bash
python3 -m venv <path_to_venv>
source <path_to_venv>/bin/activate
```

Install wheel

```bash
pip3 install wheel
```
Update pip3 and  setuptools

```bash
pip3 install --upgrade pip
pip3 install --upgrade setuptools
```

From the project root, install dependencies:

```bash
pip3 install -r requirements.txt --process-dependency-links
```

This will install a basic set of D3M primitives - those from the `common_primitves` repo, and the NK PCA Features primitive.

To run a test pipeline:

```shell
cd pipelinerunner
python3 run_pipeline.py ../test/create_pca_features.pln file:///<absolute_path_to_data>/196_autoMpg/TRAIN/dataset_TRAIN/datasetDoc.json
```

Additional primitives can be installed manually as needed. Example:

```shell
pip3 install -e git+https://github.com/NewKnowledge/simon-d3m-wrapper.git#egg=SimonD3MWrapper --process-dependency-links
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
python3 -m grpc_tools.protoc -I./proto --python_out=./pipelinerunner --grpc_python_out=./pipelinerunner --mypy_out=./pipelinerunner ./proto/*.proto
```
