FROM ubuntu:22.04

WORKDIR /project_dsa

RUN apt-get update -m -y

RUN apt-get install -y python3

RUN apt-get install -y python3-pip

COPY . /project_dsa

RUN ./install.sh

CMD [ "python3", "main.py" ]