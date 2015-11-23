FROM python:2.7-onbuild

#RUN pip install rq redis requests
#RUN pip install mrq
RUN pip install celery[redis]
RUN pip install requests

WORKDIR /usr/src/app/tasks