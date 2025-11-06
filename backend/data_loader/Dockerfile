FROM python:3.13-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /src
COPY pyproject.toml .

RUN uv lock && uv pip install --target=/deps .

FROM python:3.13-slim

RUN apt-get update && apt-get -y install --no-install-recommends \
        libpq-dev gcc python3-dev netcat-traditional \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /src
COPY --from=builder /deps /usr/local/lib/python3.13/site-packages
COPY src /src

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:$PATH"

#COPY entrypoint.sh /entrypoint.sh
#RUN chmod +x /entrypoint.sh
#
#ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
#CMD ["taskiq", "worker", "main:broker"]