ARG VERSION=latest
ARG DOCKER_REPO
FROM $DOCKER_REPO/distil-pipeline-runner-d3m:$VERSION

# Uncharted Primitives

RUN pip3 install -e git+https://github.com/uncharted-distil/distil-timeseries-loader.git@0d52a475f52848707a2b6d69fb3bae58409a784d#egg=DistilTimeSeriesLoader
RUN pip3 install -e git+https://github.com/uncharted-distil/distil-mi-ranking.git@3960299b26d52f8859917eec0cb4d8f1eaaa1c3f#egg=DistilMIRanking
RUN pip3 install -e git+https://github.com/uncharted-distil/distil-fuzzy-join.git@d171c9dc29d699dba10c1fdd5f00db8bbdd37f7d#egg=DistilFuzzyJoin

# The ta3ta2-api python package installs its own copy of the compiled protobuf files which
# conflict with those generated for this project.  Python protobuf is supposed to allow for
# multiple definitions of the same message as long as they are in different packages.  This not
# the case, so the suggested workaround is to force the use of the pure python protobuf impl,
# which doesn't enforce duplication checks as strictly as the binary implementation.
RUN pip3 uninstall -y protobuf && \
    pip3 install --no-binary=protobuf protobuf;

# done with pip - clear the cache out to save space
RUN rm -rf /root/.cache/pip

# Setup the pipeline runner source
COPY pipelinerunner ./pipelinerunner
COPY proto ./proto
COPY test ./test

ENV D3MOUTPUTDIR=/usr/local/d3m/output
ENV D3MSTATICDIR=/usr/local/d3m/static_resources
ENV PYTHONUNBUFFERED 1
ENV LD_LIBRARY_PATH=/usr/local/lib

EXPOSE 50051

CMD [ "python3", "./pipelinerunner/server.py" ]
