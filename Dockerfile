FROM python:3.8

ENV PYTHONUNBUFFERED 1

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt
