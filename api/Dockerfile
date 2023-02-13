FROM python:3.10-slim
MAINTAINER Marouane

RUN apt-get update && apt-get install -y wait-for-it curl && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y virtualenv && rm -rf /var/lib/apt/lists/*


RUN mkdir /repo 


WORKDIR /repo

COPY src/python/requirements.txt /repo
RUN pip install --upgrade -r requirements.txt


COPY src/python /repo
RUN python setup.py install
COPY src/scripts /scripts
RUN chmod +x /scripts/*

# Run
CMD /scripts/run.sh

