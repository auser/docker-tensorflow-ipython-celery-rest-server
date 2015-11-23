# FROM ermaker/keras-jupyter
FROM cuda
# FROM ubuntu:14.04

RUN apt-get update -y --fix-missing && apt-get install -q -y --no-install-recommends \
  wget bzip2 ca-certificates \
  build-essential \
  libglib2.0-0 libxext6 libsm6 libxrender1 \
  pkg-config libfreetype6-dev libXext-dev python-qt4 \
  curl grep sed dpkg  \
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
RUN pip install keras
RUN conda install -y jupyter pandas matplotlib seaborn
RUN pip install https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.5.0-cp27-none-linux_x86_64.whl

## The rest
VOLUME /notebook
WORKDIR /notebook
EXPOSE 8888
CMD jupyter notebook --no-browser --ip=0.0.0.0
