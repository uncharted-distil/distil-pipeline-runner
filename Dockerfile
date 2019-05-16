ARG VERSION=latest
ARG DOCKER_REPO
FROM $DOCKER_REPO/distil-pipeline-runner-d3m:$VERSION

# Uncharted Primitives

RUN pip3 install -e git+https://github.com/uncharted-distil/distil-timeseries-loader.git@ad36f7356d6430c1dc977176bf8ac805b37b2882#egg=DistilTimeSeriesLoader --process-dependency-links
RUN pip3 install -e git+https://github.com/uncharted-distil/distil-mi-ranking.git@7c47e32b492ef89aeac627a133b11f6699f1c22e#egg=DistilMIRanking --process-dependency-links
RUN pip3 install -e git+https://github.com/uncharted-distil/distil-fuzzy-join.git@4e860b2d9f3aa44a90a0381677aa396d265e47f7#egg=DistilFuzzyJoin --process-dependency-links

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
