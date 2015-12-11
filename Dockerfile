FROM ubuntu:latest
MAINTAINER Hive Solutions

EXPOSE 8080

ENV LEVEL INFO
ENV SERVER netius
ENV SERVER_ENCODING gzip
ENV HOST 0.0.0.0
ENV PORT 8080
ENV INSTAGRAM_ID
ENV INSTAGRAM_SECRET
ENV INSTAGRAM_REDIRECT_URL
ENV TITLE Instashow
ENV SUB_TITLE Instagram Slideshow

ADD requirements.txt /
ADD src /src

RUN apt-get update && apt-get install -y -q python python-setuptools python-dev python-pip
RUN pip install -r /requirements.txt && pip install --upgrade netius

CMD python /src/instashow/main.py
