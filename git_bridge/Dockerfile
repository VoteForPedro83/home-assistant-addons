ARG BUILD_FROM
FROM ${BUILD_FROM}

# Copy the application entry file (it lives directly in git_bridge/)
COPY app.py /app.py

# Copy s6 service definitions
COPY rootfs /

# Ensure service run script is executable (avoids GitHub exec-bit issues)
RUN chmod +x /etc/services.d/git-bridge/run

EXPOSE 8000
