FROM python:3.9-slim

WORKDIR /app

# Disable internet access
RUN echo "nameserver 0.0.0.0" > /etc/resolv.conf

# Add a non-root user
RUN useradd -m sandbox
USER sandbox

# Script to run test
COPY . .

CMD ["python", "execution_wrapper.py"]
