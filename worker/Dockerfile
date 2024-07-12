FROM python:3.11 as builder

WORKDIR /app

RUN pip install -U pip

COPY requirements.txt .
RUN pip install --root /install -r requirements.txt wait-for-it


FROM python:3.11-slim as runtime

COPY --from=builder /install /

COPY src src
COPY worker.env src/worker.env

WORKDIR /src

ENV PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV PORT=9000 \
    LOG_LEVEL="info"

CMD ["python", "main.py"]
