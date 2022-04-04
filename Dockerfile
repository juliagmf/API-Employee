FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /test
WORKDIR /test
ADD requirements.txt /test/
RUN pip install — upgrade pip && pip install -r requirements.txt
ADD . /test/