FROM ubuntu:18.04

RUN apt-get update

RUN apt-get install -y build-essential libssl-dev libcurl4-openssl-dev libffi-dev python3-dev python3-pip python3-venv git wget cmake autoconf automake libtool pkg-config libpng-dev libjpeg8-dev libtiff5-dev zlib1g-dev

RUN apt-get install -y libleptonica-dev libtesseract-dev tesseract-ocr tesseract-ocr-eng

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install wheel
RUN pip3 install grpcio
RUN pip3 install grpcio-tools googleapis-common-protos
RUN pip3 install mypy-protobuf
RUN pip3 install tensorflow
RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.0.0/en_core_web_md-2.0.0.tar.gz

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt --process-dependency-links

COPY pipelinerunner ./pipelinerunner
COPY proto ./proto
COPY test ./test

RUN python3 -m grpc_tools.protoc -I./proto --python_out=./pipelinerunner --grpc_python_out=./pipelinerunner --mypy_out=./pipelinerunner ./proto/*.proto

ENV D3MOUTPUTDIR=/usr/local/d3m/output
ENV STATIC_RESOURCE_PATH=/usr/local/d3m/static_resources
ENV PYTHONUNBUFFERED 1
ENV LD_LIBRARY_PATH=/usr/local/lib

EXPOSE 50051

CMD [ "python3", "./pipelinerunner/server.py" ]
