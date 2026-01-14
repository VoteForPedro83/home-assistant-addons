ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install python3 (and pip in case your app needs it)
RUN apk add --no-cache python3 py3-pip

# Copy the application entry file (it lives directly in git_bridge/)
COPY app.py /app.py

# Copy s6 services
COPY rootfs /

# Ensure run script is executable
RUN chmod +x /etc/services.d/git-bridge/run

EXPOSE 8000
