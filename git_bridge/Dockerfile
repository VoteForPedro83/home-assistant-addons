ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

RUN apk add --no-cache python3 py3-pip

# Create venv for Python deps (avoids PEP 668 issues)
RUN python3 -m venv /opt/venv \
  && /opt/venv/bin/pip install --no-cache-dir --upgrade pip setuptools wheel

# Set a deterministic working dir for module imports
WORKDIR /app

# Install deps into venv
COPY requirements.txt /app/requirements.txt
RUN /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Copy the app to /app/app.py so module name is "app"
COPY app.py /app/app.py

# Copy s6 services
COPY rootfs /
RUN chmod +x /etc/services.d/git-bridge/run

EXPOSE 8000
