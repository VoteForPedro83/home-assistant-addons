ARG BUILD_FROM
FROM ${BUILD_FROM}

WORKDIR /app

# Copy application code
# Your repo should contain: git_bridge/app/app.py
COPY app /app

# Copy s6 service definitions
COPY rootfs /

# Ensure service run script is executable (avoids GitHub exec-bit issues)
RUN chmod +x /etc/services.d/git-bridge/run

EXPOSE 8000
