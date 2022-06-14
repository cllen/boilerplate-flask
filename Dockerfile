FROM python:3.8

RUN mkdir -p /home/server
WORKDIR /home/server
RUN bash install.sh
