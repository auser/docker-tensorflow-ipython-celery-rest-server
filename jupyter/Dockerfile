# FROM ermaker/keras-jupyter
# FROM cuda:cudnn-runtime
#FROM kaixhin/cuda
# FROM ubuntu:14.04
FROM jupyter/minimal-notebook

## Install prereqs

## Install GPU stuff
RUN apt-get update -y && \
    apt-get install -y \
            wget \
            build-essential

# WORKDIR /usr/local/src
# RUN apt-get update -y --fix-missing && apt-get install -q -y --no-install-recommends \
#   wget bzip2 ca-certificates \
#   build-essential \
#   libglib2.0-0 libxext6 libsm6 libxrender1 \
#   pkg-config libfreetype6-dev libXext-dev python-qt4 \
#   curl grep sed dpkg git \
#   && rm -rf /var/lib/apt/lists/*

# ## Miniconda (https://hub.docker.com/r/continuumio/miniconda/~/dockerfile/)
# WORKDIR /opt
# RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
#     libglib2.0-0 libxext6 libsm6 libxrender1
# RUN echo 'export PATH=/usr/local/src/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
#     wget --quiet https://repo.continuum.io/archive/Anaconda2-2.4.0-Linux-x86_64.sh && \
#     pwd && ls -l && \
#     /bin/bash Anaconda2-2.4.0-Linux-x86_64.sh -b -p /opt/conda && \
#     rm /opt/Anaconda2-2.4.0-Linux-x86_64.sh && \
#     /opt/conda/bin/conda install --yes conda==3.18.3

# RUN apt-get install -y curl grep sed dpkg && \
#     TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
#     curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
#     dpkg -i tini.deb && \
#     rm tini.deb && \
#     apt-get clean

# ENV PATH /opt/conda/bin:$PATH

# # http://bugs.python.org/issue19846
# # > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
# ENV LANG C.UTF-8

# ENTRYPOINT [ "/usr/bin/tini", "--" ]
##

# iPython stuff
RUN conda install -y theano h5py
RUN pip install keras ipyparallel sklearn
RUN conda install -y jupyter pandas matplotlib seaborn

## Install tensorflow

# RUN pip install https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.5.0-cp27-none-linux_x86_64.whl

## mxnet
WORKDIR /usr/local/src
RUN apt-get install -y build-essential git libatlas-base-dev libopencv-dev python-opencv
RUN git clone --recursive https://github.com/dmlc/mxnet
RUN cd mxnet; make -j4

## Torch kernel
WORKDIR /usr/local/src
RUN sudo apt-get install -y libzmq3-dev \
             luarocks libssl-dev  cmake graphviz \
             libqtgui4:amd64

## From https://hub.docker.com/r/kaixhin/cuda-torch/~/dockerfile/
# Run Torch7 installation scripts
RUN curl -sk https://raw.githubusercontent.com/torch/ezinstall/master/install-deps | bash
RUN git clone https://github.com/torch/distro.git ~/torch --recursive
RUN cd ~/torch; ./install.sh

# Set ~/torch as working directory
WORKDIR /root/torch

# Export environment variables manually
ENV LUA_PATH='/root/.luarocks/share/lua/5.1/?.lua;/root/.luarocks/share/lua/5.1/?/init.lua;/root/torch/install/share/lua/5.1/?.lua;/root/torch/install/share/lua/5.1/?/init.lua;./?.lua;/root/torch/install/share/luajit-2.1.0-alpha/?.lua;/usr/local/share/lua/5.1/?.lua;/usr/local/share/lua/5.1/?/init.lua' \
  LUA_CPATH='/root/.luarocks/lib/lua/5.1/?.so;/root/torch/install/lib/lua/5.1/?.so;./?.so;/usr/local/lib/lua/5.1/?.so;/usr/local/lib/lua/5.1/loadall.so' \
  PATH=/root/torch/install/bin:$PATH \
  LD_LIBRARY_PATH=/root/torch/install/lib:$LD_LIBRARY_PATH \
  DYLD_LIBRARY_PATH=/root/torch/install/lib:$DYLD_LIBRARY_PATH

CMD ["/root/torch/install/bin/th"]

WORKDIR /root/torch

RUN /usr/bin/luarocks install lzmq
RUN /usr/bin/luarocks install penlight
RUN /usr/bin/luarocks install luafilesystem
RUN /usr/bin/luarocks install luacrypto
#RUN /usr/bin/luarocks install qlua

RUN git clone https://github.com/torch/graph.git
WORKDIR $HOME/torch/graph/rocks
CMD ["/usr/bin/luarocks make"]

RUN git clone git://github.com/koraykv/torch-nngraph.git
WORKDIR $HOME/torch/nn-graph
CMD ["/usr/bin/luarocks make"]

RUN git clone https://github.com/torch/cunn.git
WORKDIR $HOME/torch/cunn/rocks
CMD ["/usr/bin/luarocks make"]

#RUN /usr/bin/luarocks install optim
#RUN /usr/bin/luarocks install nn
#RUN /usr/bin/luarocks install cltorch
#RUN /usr/bin/luarocks install clnn

RUN luarocks install qtlua

WORKDIR $HOME/torch
RUN git clone https://github.com/facebook/iTorch.git
WORKDIR $HOME/torch/iTorch
CMD ["/usr/bin/luarocks make"]


## TODO: Move above
VOLUME /notebook
WORKDIR /notebook

#RUN useradd -d /notebook -ms /bin/bash nonroot

#RUN chown -R nonroot:nonroot /notebook
#USER nonroot
#ENV HOME /notebook

## The rest
EXPOSE 8888
#CMD itorch notebook --no-browser --ip=0.0.0.0 --profile=itorch
CMD jupyter notebook --no-browser --ip=0.0.0.0 --config=/.jupyter/jupyter_notebook_config.py
