# Use an official Ubuntu image as a parent image
FROM ubuntu:latest

# Install necessary packages (e.g., Python, Redis, MongoDB, and other dependencies)
RUN apt-get update \
    && apt-get install -y python3 python3-pip redis-server screen \
    && apt-get install -y gnupg curl \
    && apt-get install -y chromium-browser

# Import MongoDB GPG key
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-archive-keyring.gpg

# Add MongoDB repository to sources list
RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-archive-keyring.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update package lists and install MongoDB
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y mongodb-org \
    && rm -rf /var/lib/apt/lists/*

# Create a directory for MongoDB data
RUN mkdir -p /data/db

# Set the working directory in the container
WORKDIR /AwesomeBioVault

# Copy the current directory contents into the container at /AwesomeBioVault
COPY . /AwesomeBioVault

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements/prod.txt

# Expose Redis default port
EXPOSE 6379

# Expose MongoDB default port
EXPOSE 27017

# Expose your application port
EXPOSE 5001

# Run screens for all servers
CMD ["sh", "-c", "screen -dmS servers && screen -S servers -X screen -t web sh -c 'gunicorn -w 4 -b 0.0.0.0:5001 app.app:app'; screen -S servers -X screen -t celery sh -c 'celery -A app.api.V1.endpoints.utils worker --loglevel=info'; screen -S servers -X screen -t redis sh -c 'redis-server'; screen -S servers -X screen -t mongo sh -c 'mongod'"]
