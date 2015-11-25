# FROM ermaker/keras-jupyter
# FROM cuda:cudnn-runtime
FROM kaixhin/cuda
# FROM ubuntu:14.04

## Install prereqs

RUN cd /usr/local/src
RUN apt-get update -y --fix-missing && apt-get install -q -y --no-install-recommends \
  wget bzip2 ca-certificates \
  build-essential \
  libglib2.0-0 libxext6 libsm6 libxrender1 \
  pkg-config libfreetype6-dev libXext-dev python-qt4 \
  curl grep sed dpkg git \
  && rm -rf /var/lib/apt/lists/*

## Miniconda (https://hub.docker.com/r/continuumio/miniconda/~/dockerfile/)
RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/archive/Anaconda2-2.4.0-Linux-x86_64.sh && \
    /bin/bash /Anaconda2-2.4.0-Linux-x86_64.sh -b -p /opt/conda && \
    rm /Anaconda2-2.4.0-Linux-x86_64.sh && \
    /opt/conda/bin/conda install --yes conda==3.18.3

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

ENV PATH /opt/conda/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

ENTRYPOINT [ "/usr/bin/tini", "--" ]
##

# iPython stuff
RUN conda install -y theano h5py
RUN pip install keras ipyparallel
RUN conda install -y jupyter pandas matplotlib seaborn
RUN pip install https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.5.0-cp27-none-linux_x86_64.whl

## mxnet
RUN apt-get install -y build-essential git libatlas-base-dev libopencv-dev python-opencv
RUN cd /usr/local/src
RUN git clone --recursive https://github.com/dmlc/mxnet
RUN cd mxnet; make -j4

## Torch kernel
RUN cd /usr/local/src
RUN sudo apt-get install libzmq3-dev luarocks openssl cmake

RUN curl -s https://raw.githubusercontent.com/torch/ezinstall/master/install-deps | bash
RUN git clone https://github.com/torch/distro.git /usr/local/src/torch --recursive
RUN cd /usr/local/src/torch; ./install.sh


RUN cd /usr/local/src
RUN git clone https://github.com/facebook/iTorch.git
RUN cd iTorch
RUN luarocks install lzmq
RUN luarocks install penlight
RUN luarocks install luafilesystem
RUN luarocks install luacrypto
RUN luarocks install org.conman.env
RUN luarocks make


## The rest
VOLUME /notebook
WORKDIR /notebook
EXPOSE 8888
CMD jupyter notebook --no-browser --ip=0.0.0.0
