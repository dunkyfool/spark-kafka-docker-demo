# TOOLHIT (Ubuntu 16.04)

FROM ubuntu:16.04

# Install python, pip
RUN apt-get update && \
    apt-get install -y python && \
    apt-get install -y python-pip python-dev build-essential && \
    apt-get install -y librdkafka-dev && \
    apt-get install -y vim && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Upgrade pip & Install pykafka, redis, numpy
RUN pip install --upgrade pip && \
    pip install numpy && \
    pip install pykafka && \
    pip install redis

#ADD scripts/start-kafka.sh /usr/bin/start-kafka.sh

#CMD ["supervisord", "-n"]
