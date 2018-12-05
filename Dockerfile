FROM ubuntu:18.04

RUN apt-get update

RUN apt-get install -y build-essential libssl-dev libcurl4-openssl-dev libffi-dev python3-dev python3-pip python3-venv git wget cmake autoconf automake libtool pkg-config libpng-dev libjpeg8-dev libtiff5-dev zlib1g-dev

# external dependencies for NK CROC primitive
RUN apt-get install -y libleptonica-dev libtesseract-dev tesseract-ocr tesseract-ocr-eng

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install wheel
RUN pip3 install grpcio
RUN pip3 install grpcio-tools googleapis-common-protos
RUN pip3 install mypy-protobuf

RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.0.0/en_core_web_md-2.0.0.tar.gz

# Using the requirements file results in a single cache layer for python packages and
# dependencies, which makes the image build very slowly when a new python package is added.
# As an optimization, we intentionally run package installation as a manual set of RUN
# commands, and ignore the requirements.txt file.  We could template this Dockerfile
# and have the build.sh script copy the contents of the requirements file in to reduce
# duplication.
#
# COPY requirements.txt ./requirements.txt
# RUN pip3 install -r requirements.txt --process-dependency-links

RUN pip install torch
RUN pop install 'imageio<2.4.0'
# D3M baseline packages - do this first because there are a lot of dependencies
RUN pip install -e git+https://gitlab.com/datadrivendiscovery/common-primitives.git@3bf21226aff90a826cf36b8b9694cedb81ff6357#egg=common_primitives --process-dependency-links --no-deps
RUN pip install -e git+https://gitlab.com/datadrivendiscovery/d3m.git@f34bf97e8fe4ce78397adcfc291ddca778a34b5f#egg=d3m --process-dependency-links

# NK Primitives
RUN pip install -e git+https://github.com/NewKnowledge/croc-d3m-wrapper.git@2ba83b47ec207f1d04ba1e5009d94d30987ea396#egg=CrocD3MWrapper --process-dependency-links
RUN pip install -e git+https://github.com/NewKnowledge/pcafeatures-d3m-wrapper.git@5ec8cf9d0288bc1f581e7e44f1b61ce73ceaeefd#egg=PcafeaturesD3MWrapper --process-dependency-links
RUN pip install -e git+https://github.com/NewKnowledge/simon-d3m-wrapper.git@8845285e63116ca6ac814b7ef6d7af696447e305#egg=SimonD3MWrapper --process-dependency-links
# revert to NK version once fixes are merged
RUN pip install -e git+https://github.com/NewKnowledge/duke-d3m-wrapper.git@0b1495d6f34dc828011d9d55be2b42917c5b67d8#egg=DukeD3MWrapper --process-dependency-links
#-e git+https://github.com/NewKnowledge/unicorn-d3m-wrapper.git@7318a8354cbc6f336e08f26c14e6b372d7b5a10c#egg=UnicornD3MWrapper --process-dependency-links
RUN pip install -e git+https://github.com/cdbethune/unicorn-d3m-wrapper.git@c843fe7f3d18240331eb785862b8880aeff707be#egg=UnicornD3MWrapper --process-dependency-links
# cython isn't installing as  transitive dependency for some reason
RUN pip install cython
RUN pip install -e git+https://github.com/cdbethune/sloth-d3m-wrapper.git@aa1beac603ff73b4d3231088a26ad3d4a9e53725#egg=SlothD3MWrapper --process-dependency-links



# Uncharted Primitives

# Setup for private repo access
ARG SSH_KEY
RUN mkdir -p /root/.ssh
RUN echo "${SSH_KEY}" > /root/.ssh/id_rsa
RUN chmod 0600 /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN pip install -e git+ssh://git@github.com/unchartedsoftware/distil-timeseries-loader.git@271483e6c4f884a2f49c246ca51490b94f5ff88b#egg=DistilTimeSeriesLoader --process-dependency-links
RUN pip install -e git+ssh://git@github.com/unchartedsoftware/distil-mi-ranking.git@16b1be14cb80ff14a80cd5db99eb2057b44098e1#egg=DistilMIRanking --process-dependency-links

# Get rid of the access key.
# ** NOTE: ** if build without --squash arg this will still be in the
# image history.  This is a read only key for a low importance repo
# so not a huge issue if it leaks.
RUN rm /root/.ssh/id_rsa

# Setup the pipeline runner source
COPY pipelinerunner ./pipelinerunner
COPY proto ./proto
COPY test ./test
RUN python3 -m grpc_tools.protoc \
    -I./proto/ta3ta2-api \
    -I./proto \
    --python_out=./pipelinerunner \
    --grpc_python_out=./pipelinerunner \
    --mypy_out=./pipelinerunner \
    ./proto/ta3ta2-api/value.proto \
    ./proto/ta3ta2-api/primitive.proto \
    ./proto/ta3ta2-api/pipeline.proto \
    ./proto/execute.proto

ENV D3MOUTPUTDIR=/usr/local/d3m/output
ENV STATIC_RESOURCE_PATH=/usr/local/d3m/static_resources
ENV PYTHONUNBUFFERED 1
ENV LD_LIBRARY_PATH=/usr/local/lib

EXPOSE 50051

CMD [ "python3", "./pipelinerunner/server.py" ]
