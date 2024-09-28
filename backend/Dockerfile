FROM python:alpine

WORKDIR /app

RUN apk update && apk add --no-cache \
    libpq-dev \
    postgresql-dev \
    python3-dev \
    build-base \
    bash

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
#CMD ["tail", "-f", "/dev/null"]
