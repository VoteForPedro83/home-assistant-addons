ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.20
FROM ${BUILD_FROM}

# Install Python and virtualenv
RUN apk add --no-cache python3 py3-pip py3-virtualenv

# Create Python virtual environment (PEP 668 safe)
RUN python3 -m venv /opt/venv \
  && /opt/venv/bin/pip install --upgrade pip \
  && /opt/venv/bin/pip install fastapi uvicorn requests

# Use venv by default
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY app.py /app/app.py
COPY run.sh /app/run.sh

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
