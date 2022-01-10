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
    vim \
  && apt clean

WORKDIR /apps/
RUN git clone https://github.com/broadinstitute/cromshell.git && \
  cp cromshell/cromshell /usr/local/bin/ && \
  rm -rf cromshell

WORKDIR /apps/build/
COPY ./ ./
RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install --prefix=/usr/local .
RUN mv ./jar/ /apps/cromwell/
WORKDIR /apps/
RUN find . -type d -exec chmod go+w {} \; && \
  find . -type f -exec chmod go+w {} \;
RUN rm -rf /apps/build/

ENV TZ America/Chicago
ENV LANG C
WORKDIR /
