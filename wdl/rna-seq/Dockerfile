# Dockerfile for ENCODE-DCC rna-seq-pipeline
FROM ubuntu@sha256:2695d3e10e69cc500a16eae6d6629c803c43ab075fa5ce60813a0fc49c47e859
LABEL MAINTAINER Eddie Belter

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
  apt install -y \
    bzip2 \
    ghostscript \
    git \
    libncurses5-dev \
    libnss-sss \
    python3-dev \
    python3-pip \
    r-base-core \
    unzip \
    wget && \
    apt clean 

RUN pip3 install pandas==0.24.2
RUN pip3 install pysam==0.15.3

# Stick to Jin's way of organizing the directory structure
WORKDIR /apps

# Install STAR/Samtools dependencies
RUN wget http://zlib.net/zlib-1.2.12.tar.gz && tar -xvf zlib-1.2.12.tar.gz
RUN cd zlib-1.2.12 && ./configure && make && make install && rm ../zlib-1.2.12.tar.gz

RUN wget https://tukaani.org/xz/xz-5.2.3.tar.gz && tar -xvf xz-5.2.3.tar.gz
RUN cd xz-5.2.3 && ./configure && make && make install && rm ../xz-5.2.3.tar.gz

# Install STAR
ARG STAR_VERSION="2.7.9a"
RUN wget https://github.com/alexdobin/STAR/archive/refs/tags/${STAR_VERSION}.tar.gz && tar -xzf ${STAR_VERSION}.tar.gz
RUN cd STAR-${STAR_VERSION}/source && make STAR && cd ../.. && rm ${STAR_VERSION}.tar.gz

# Install Samtools 1.9
RUN git clone --branch 1.9 --single-branch https://github.com/samtools/samtools.git && \
    git clone --branch 1.9 --single-branch https://github.com/samtools/htslib.git && \
    cd samtools && make && make install && cd ../ && rm -rf samtools* htslib*

# Install kentutils 385
RUN git clone https://github.com/ENCODE-DCC/kentutils_v385_bin_bulkrna.git

# Install qc-utils 19.8.1 and ptools
RUN pip3 install qc-utils==19.8.1 ptools_bin==0.0.7

WORKDIR /apps/scripts/
COPY scripts/ ./

ENV PATH="/apps/STAR-${STAR_VERSION}/bin/Linux_x86_64:/apps/kentutils_v385_bin_bulkrna:/apps/scripts:/apps:${PATH}"
