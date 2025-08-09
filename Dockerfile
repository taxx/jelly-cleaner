FROM python:3.11-slim

WORKDIR /app

COPY main.py ./
COPY jellyseerr_client.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get update && apt-get install -y cron

# Run main.py once at container startup, then start cron
CMD ["/bin/bash", "-c", "cd /app && /usr/local/bin/python main.py >> /var/log/cron.log 2>&1; crontab /app/crontab && cron && touch /var/log/cron.log && tail -f /var/log/cron.log"]