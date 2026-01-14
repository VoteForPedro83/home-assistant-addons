ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install python and build deps for common wheels
RUN apk add --no-cache python3 py3-pip

# Copy requirements and install Python deps
COPY requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

# Copy application entry file (it lives directly in git_bridge/)
COPY app.py /app.py

# Copy s6 services
COPY rootfs /

# Ensure run script is executable
RUN chmod +x /etc/services.d/git-bridge/run

EXPOSE 8000
