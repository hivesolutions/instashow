FROM ubuntu:latest
MAINTAINER Hive Solutions

RUN apt-get update && apt-get install -y -q python python-setuptools python-dev git
RUN easy_install pip && pip install flask quorum netius instagram_api
RUN git clone https://github.com/hivesolutions/instashow

ENV SERVER netius
ENV SERVER_ENCODING gzip
ENV HOST 0.0.0.0
ENV PORT 8080

ENTRYPOINT ["usr/bin/python", "instashow/src/instashow/main.py"]
