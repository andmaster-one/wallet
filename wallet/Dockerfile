FROM python:3.9.0
WORKDIR /code/
RUN mkdir db/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install --no-cache-dir -r req.txt
COPY . .
