FROM python:3.12

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpg-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY /requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .


EXPOSE 8000