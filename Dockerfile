FROM python:3.8-slim

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install ffmpeg

RUN mkdir /shamebot

COPY requirements.txt /shamebot/
RUN python3 -m pip install -r /shamebot/requirements.txt

COPY resources /shamebot/resources
COPY config.json shame.py /shamebot/

WORKDIR /shamebot

CMD [ "python3", "shame.py" ]
