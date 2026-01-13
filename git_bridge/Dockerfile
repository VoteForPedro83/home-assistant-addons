ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.20
FROM ${BUILD_FROM}

RUN apk add --no-cache python3 py3-pip py3-virtualenv

RUN python3 -m venv /opt/venv \
  && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
  && /opt/venv/bin/pip install --no-cache-dir fastapi uvicorn requests

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY app.py /app/app.py

# Add s6 service files
COPY rootfs/ /

RUN chmod +x /etc/services.d/git-bridge/run

# FORCE s6 init as PID 1 (important)
ENTRYPOINT ["/init"]
