FROM ubuntu:16.04

# ENV
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle
ENV SPARK_HOME=/opt/spark-1.6.0
ENV PATH=$SPARK_HOME:$PATH
ENV PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH

# Install Java, git, python, librdkafka, vim, scala, spark
RUN \
  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  apt-get update && \
  apt-get install -y  software-properties-common && \
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y oracle-java8-installer && \
  apt-get install -y git && \
  apt-get install -y python && \
  apt-get install -y python-pip python-dev build-essential && \
  apt-get install -y librdkafka-dev && \
  apt-get install -y vim && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /var/cache/oracle-jdk8-installer && \
  apt-get clean && \
  wget -q http://www.scala-lang.org/files/archive/scala-2.11.7.deb -O /tmp/scala-2.11.7.deb && \
  dpkg -i /tmp/scala-2.11.7.deb && \
  rm /tmp/scala-2.11.7.deb && \
  wget -q http://d3kbcqa49mib13.cloudfront.net/spark-1.6.0.tgz -O /tmp/spark-1.6.0.tgz && \
  tar xvf /tmp/spark-1.6.0.tgz -C /opt && \
  rm /tmp/spark-1.6.0.tgz && \
  cd /opt/spark-1.6.0 && \
  sbt/sbt assembly 

# Upgrade pip & Install pykafka, redis, numpy
RUN pip install --upgrade pip && \
    pip install numpy && \
    pip install pykafka && \
    pip install redis && \
    pip install py4j

# Define working directory.
WORKDIR /data
