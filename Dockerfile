FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# --- system dependencies (only what cochlea actually needs) ---
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3.8-dev \
    python3-pip \
    build-essential \
    gfortran \
    libsndfile1 \
    libfftw3-dev \
    && rm -rf /var/lib/apt/lists/*

# --- make python3.8 the default ---
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

# --- python packages (minimal set you asked for) ---
RUN pip3 install --upgrade pip \
 && pip3 install \
    numpy \
    scipy \
    matplotlib \
    Cython \
    cochlea \
    thorns
