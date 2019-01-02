FROM docker.uncharted.software/distil-pipeline-runner-d3m:latest

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
RUN pip install -e git+ssh://git@github.com/unchartedsoftware/distil-fuzzy-join.git@d2c03783f517398e7fb32817fcaac9e0e09d660e#egg=DistilFuzzyJoin --process-dependency-links

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
