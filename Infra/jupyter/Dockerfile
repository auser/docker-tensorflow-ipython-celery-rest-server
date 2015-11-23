FROM ermaker/keras-jupyter

RUN apt-get update -y
RUN apt-get install -y pkg-config libfreetype6-dev libXext-dev python-qt4

RUN conda install -y jupyter pandas matplotlib seaborn

VOLUME /notebook
WORKDIR /notebook
EXPOSE 8888
CMD jupyter notebook --no-browser --ip=0.0.0.0
