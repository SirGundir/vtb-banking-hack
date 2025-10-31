FROM python:3.13-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN uv pip install --target=/deps .

FROM python:3.13-slim

RUN apt-get update && apt-get -y install --no-install-recommends \
        libpq-dev gcc python3-dev netcat-traditional \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY --from=builder /deps /usr/local/lib/python3.13/site-packages
COPY src /app/src

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

RUN chmod +x /app/src/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/app/src/entrypoint.sh"]