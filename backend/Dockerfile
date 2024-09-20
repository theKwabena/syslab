FROM python:alpine

WORKDIR /app

RUN apk update && apk add --no-cache \
    libpq-dev \
    postgresql-dev \
    python3-dev \
    build-base

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]