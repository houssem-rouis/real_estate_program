ARG BASE_IMAGE
FROM $BASE_IMAGE

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

ADD . /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000