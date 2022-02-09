FROM python:latest

RUN apt update && apt install pip -y && python -m pip install --upgrade pip

ADD req.txt /

RUN pip install -r req.txt

WORKDIR /wildberries

ADD wildberries /wildberries/

# RUN cd wildberries && python scrapy crawl wb