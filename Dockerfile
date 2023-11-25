# Use an official Ubuntu image as a parent image
FROM ubuntu:latest

# Install necessary packages (e.g., Python, Redis, and other dependencies)
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    redis-server \
    screen \
    gnupg \
    curl \
    chromium-browser

# Set the working directory in the container
WORKDIR /AwesomeBioVault

# Copy the current directory contents into the container at /AwesomeBioVault
COPY . /AwesomeBioVault

# Set environment variable for Puppeteer
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# Install packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements/prod.txt

# Expose ports
EXPOSE 6379 5001

# Use supervisord to manage multiple processes
RUN apt-get update && \
    apt-get install -y supervisor && \
    rm -rf /var/lib/apt/lists/*
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# CMD can be changed to run supervisord which will manage all services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
