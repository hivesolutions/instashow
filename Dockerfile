FROM ubuntu:latest
MAINTAINER Hive Solutions

RUN apt-get update && apt-get install -y -q python python-setuptools git
RUN easy_install pip && pip install flask quorum instagram_api
RUN git clone https://github.com/hivesolutions/instashow

ENTRYPOINT ["usr/bin/python", "instashow/src/instashow.py"]
