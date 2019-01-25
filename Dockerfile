FROM docker.uncharted.software/distil-pipeline-runner-d3m:latest

# Uncharted Primitives

# Setup for private repo access
ARG SSH_KEY
RUN mkdir -p /root/.ssh
RUN echo "${SSH_KEY}" > /root/.ssh/id_rsa
RUN chmod 0600 /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN pip3 install -e git+ssh://git@github.com/unchartedsoftware/distil-timeseries-loader.git@5dd90e7426dab210d8312ec8cd9e01bb87fcf955#egg=DistilTimeSeriesLoader --process-dependency-links
RUN pip3 install -e git+https://github.com/unchartedsoftware/distil-mi-ranking.git@7c47e32b492ef89aeac627a133b11f6699f1c22e#egg=DistilMIRanking --process-dependency-links
RUN pip3 install -e git+ssh://git@github.com/unchartedsoftware/distil-fuzzy-join.git@0a9ecb2e557e6d69905ae047899903c6211a1674#egg=DistilFuzzyJoin --process-dependency-links

# done with pip - clear the cache out to save space
RUN rm -rf /root/.cache/pip

# Get rid of the access key.
# ** NOTE: ** if build without --squash arg this will still be in the
# image history.  This is a read only key for a low importance repo
# so not a huge issue if it leaks.
RUN rm /root/.ssh/id_rsa

# Setup the pipeline runner source
COPY pipelinerunner ./pipelinerunner
COPY proto ./proto
COPY test ./test

ENV D3MOUTPUTDIR=/usr/local/d3m/output
ENV STATIC_RESOURCE_PATH=/usr/local/d3m/static_resources
ENV PYTHONUNBUFFERED 1
ENV LD_LIBRARY_PATH=/usr/local/lib

EXPOSE 50051

CMD [ "python3", "./pipelinerunner/server.py" ]
