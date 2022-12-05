FROM ubuntu:18.04

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install docker
RUN apt-get update && \
    apt-get -qy full-upgrade && \
    apt-get install -qy curl && \
    curl -sSL https://get.docker.com/ | sh

# install python and pip
RUN apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt install python3.8 -y && \
    apt install python3-pip -y 

WORKDIR /app

COPY requirements.txt /app/
COPY ./core /app/

RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "sh", "-c", "python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000" ]

