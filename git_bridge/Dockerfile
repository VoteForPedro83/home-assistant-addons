ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.20
FROM ${BUILD_FROM}

# Ensure s6 overlay is PID 1 (prevents "s6-overlay-suexec: can only run as pid 1")
ENTRYPOINT ["/init"]

# Python + venv support
RUN apk add --no-cache python3 py3-pip py3-virtualenv

# Create and use a venv so pip installs are allowed (avoids PEP 668)
RUN python3 -m venv /opt/venv \
  && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
  && /opt/venv/bin/pip install --no-cache-dir fastapi uvicorn requests

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY app.py /app/app.py

# HA add-on s6 services
COPY rootfs/ /
RUN chmod +x /etc/services.d/git-bridge/run
