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

Update pip3 and setuptools

```bash
pip3 install --upgrade pip
pip3 install --upgrade setuptools
```

Setup GRPC:

```shell
pip3 install grpcio
pip3 install grpcio-tools googleapis-common-protos
pip3 install mypy-protobuf

# bug in binary grpc with name collisions - force use of software version
pip3 uninstall grpc -y protobuf
pip3 install --no-binary=protobuf protobuf
```

Clone this directory, and from the project root pull the TA3TA2 API files:

```shell
git clone github@github.com:unchartedsoftware/distil-pipeline-runner.git
git submodule init
git submodule update
cd distil-pipeline-runner
```

Finally, install dependencies (this can take a while):

```bash
pip3 install -r requirements.txt --process-dependency-links
```

To run a test pipeline:

```shell
python3 ./pipelinerunner/run_pipeline.py ./test/pca_features.pln file:///<absolute_path_to_data>/196_autoMpg/TRAIN/dataset_TRAIN/datasetDoc.json
```

You can add `-r <path_to_static_resource_directory>` and `-v` to the end of the run command above, for static resource use and verbose output from each primitive.  The input file can either be serialized protobuf (.pln) or JSON (.json).

To convert a protobuf pipeline to JSON:

```shell
python3 ./pipelinerunner/proto_to_json.py ./test/pca_features.pln pca_features.json
```

To convert a JSON pipeline protobuf:

```shell
python3 ./pipelinerunner/json_to_proto.py ./test/pca_features.json pca_features.pln
```

Additional primitives can be installed manually as needed. Example:

```shell
pip3 install -e git+https://github.com/NewKnowledge/simon-d3m-wrapper.git#egg=SimonD3MWrapper --process-dependency-links
```

[OPTIONAL] To re-generate the protobuf files and MyPy type definitions for them:

```shell
cd proto/ta3ta2_api
git checkout devel
cd ../..
./gen_proto.sh
```

This should only be necessary if `proto/execute.proto` is modified and needs to be rebuilt, or the `proto/ta3ta2-api` files have been moved to a new version.
