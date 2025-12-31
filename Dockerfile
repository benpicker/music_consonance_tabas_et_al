FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# --- system dependencies ---
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3.8-dev \
    python3-pip \
    build-essential \
    gfortran \
    libsndfile1 \
    libfftw3-dev \
    && rm -rf /var/lib/apt/lists/*

# --- make python3.8 default ---
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

# --- upgrade pip ---
RUN pip3 install --upgrade pip

# --- install build-time deps (PIN CYTHON) ---
RUN pip3 install \
    numpy \
    scipy \
    matplotlib \
    Cython==0.29.36

# --- now install cochlea and thorns ---
RUN pip3 install \
    cochlea \
    thorns

# --- set working directory inside container ---
WORKDIR /workspace

# --- copy entire project into the image (disabled for local volume mounting) ---
# COPY . /workspace
