FROM python:3.10.0-buster

RUN apt update && \
  apt install -y \
    bsdmainutils \
    curl \
    default-jdk \
    git \
    jq \
    less \
    libnss-sss \
    mailutils \
    sqlite3 \
    vim \
    zip \
  && apt clean

ARG CROMWELL_VERSION=81
WORKDIR /apps/cromwell/
RUN wget -nv "https://github.com/broadinstitute/cromwell/releases/download/${CROMWELL_VERSION}/cromwell-${CROMWELL_VERSION}.jar" && \
  mv cromwell-${CROMWELL_VERSION}.jar cromwell.jar
RUN wget -nv "https://github.com/broadinstitute/cromwell/releases/download/${CROMWELL_VERSION}/womtool-${CROMWELL_VERSION}.jar" && \
  mv womtool-${CROMWELL_VERSION}.jar womtool.jar

WORKDIR /apps/build/
COPY ./ ./
RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install --prefix=/usr/local .

WORKDIR /apps/
RUN mv /apps/build/twlab-pipelines/wdl/ ./
WORKDIR /apps/wdl/bulk-rna/
RUN mv /apps/build/hprc-benchmarking/bulk-rna/build-idxs.* .
RUN mv /apps/build/hprc-benchmarking/bulk-rna/rna-seq-pipeline.* .

WORKDIR /apps/
RUN rm -rf /apps/build/
RUN find . -type f -exec chmod -R go+rw {} \; && \
  find . -type d -exec chmod -R go+rwx {} \;

ENV TZ America/Chicago
ENV LANG C
WORKDIR /
