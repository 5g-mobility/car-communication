FROM ubuntu:18.04
WORKDIR /code

ENV SUMO_VERSION 1.9.0
ENV SUMO_HOME /opt/sumo

# Install system dependencies.
RUN apt-get update && apt-get -qq install \
    wget \
    g++ \
    make \
    libxerces-c-dev \
    libfox-1.6-0 libfox-1.6-dev \
    python2.7 

RUN apt-get update && apt-get -qq install software-properties-common

RUN add-apt-repository ppa:sumo/stable

RUN apt-get update && apt-get -qq install sumo sumo-tools sumo-doc

RUN wget http://downloads.sourceforge.net/project/sumo/sumo/version%20$SUMO_VERSION/sumo-src-$SUMO_VERSION.tar.gz
RUN tar xzf sumo-src-$SUMO_VERSION.tar.gz && \
    mv sumo-$SUMO_VERSION $SUMO_HOME && \
    rm sumo-src-$SUMO_VERSION.tar.gz


RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8 

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt remove python3-pip
RUN apt-get update && apt-get -qq install python3.8 python3.8-dev python3.8-distutils python3.8-venv python3-setuptools curl

RUN python3.8 -m venv venv
RUN . venv/bin/activate
COPY requirements.txt /code/
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py
RUN python3.8 -m pip install -r requirements.txt
COPY . /code/