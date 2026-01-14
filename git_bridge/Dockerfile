ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

# System packages
RUN apk add --no-cache python3 py3-pip

# Create an isolated venv so we don't violate PEP 668
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

# Install Python deps into the venv
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copy app (app.py lives directly in git_bridge/)
COPY app.py /app.py

# Copy s6 services
COPY rootfs /
RUN chmod +x /etc/services.d/git-bridge/run

EXPOSE 8000
