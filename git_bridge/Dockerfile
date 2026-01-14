ARG BUILD_FROM
FROM ${BUILD_FROM}

# App entrypoint lives directly in git_bridge/
COPY app.py /app.py

# s6 services
COPY rootfs /

# Ensure run script is executable
RUN chmod +x /etc/services.d/git-bridge/run

EXPOSE 8000
