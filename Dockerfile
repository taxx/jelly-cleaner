FROM python:3.11-slim

WORKDIR /app

COPY main.py ./
COPY jellyseerr_client.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get update && apt-get install -y cron

# Start cron, install crontab from /app/crontab, and keep container running
CMD ["/bin/bash", "-c", "crontab /app/crontab && cron && touch /var/log/cron.log && tail -f /var/log/cron.log"]