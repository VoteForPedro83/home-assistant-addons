ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

# System packages
RUN apk add --no-cache python3 py3-pip

# App directory
WORKDIR /app

# Create venv (avoids PEP 668 issues) and upgrade installer tooling
RUN python3 -m venv /opt/venv \
  && /opt/venv/bin/pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python deps into the venv
COPY requirements.txt /app/requirements.txt
RUN /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Copy app (now placed at /app/app.py so module name "app" is unambiguous)
COPY app.py /app/app.py

# Copy s6 services
COPY rootfs /
RUN chmod +x /etc/services.d/git-bridge/run

EXPOSE 8000
