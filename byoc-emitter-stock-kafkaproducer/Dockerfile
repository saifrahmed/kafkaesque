FROM python:3.6-alpine

MAINTAINER Saif Ahmed <sahmed@kinetica.com>

ADD requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /work

ADD mumbler-stock.py /work/mumbler-stock.py
CMD [ "python","/work/mumbler-stock.py" ]
