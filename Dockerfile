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
RUN wget "https://github.com/broadinstitute/cromwell/releases/download/${CROMWELL_VERSION}/cromwell-${CROMWELL_VERSION}.jar" && \
  mv cromwell-${CROMWELL_VERSION}.jar cromwell.jar
RUN wget "https://github.com/broadinstitute/cromwell/releases/download/${CROMWELL_VERSION}/womtool-${CROMWELL_VERSION}.jar" && \
  mv womtool-${CROMWELL_VERSION}.jar womtool.jar

WORKDIR /apps/cromshell/
RUN git clone https://github.com/broadinstitute/cromshell.git && \
  sed -i 's#\${HOME}#/apps/cromshell#' cromshell/cromshell && \
  cp cromshell/cromshell /usr/local/bin/ && \
  rm -rf cromshell
WORKDIR /apps/cromshell/.cromshell/

WORKDIR /apps/build/
COPY ./ ./
RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install --prefix=/usr/local .
RUN mv ./wdl/ /apps/
WORKDIR /apps/
RUN rm -rf /apps/build/
RUN chmod -R go+w .

ENV TZ America/Chicago
ENV LANG C
WORKDIR /
