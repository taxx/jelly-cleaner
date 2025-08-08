# Jellyseerr Media Cleaner

This Python tool automatically deletes old movies and TV shows that were previously requested through Jellyseerr.

It's useful for home media servers with limited space and supports:
- Per-user whitelisting (media is never deleted if requested by whitelisted users)
- Dry-run mode (safe preview of what would be deleted)

---

## 🚀 Features

- Deletes **Movies and TV shows**
- Skips requests by **whitelisted users**
- Uses **Jellyseerr API**, expects to us cookie based auth with a jellyseer user with correct permissions
- Supports **dry-run** mode (no actual deletion)

---

## 🛠️ Requirements

- Python 3.8+
- Access to your Jellyseerr, Sonarr, and Radarr APIs
- API keys for all three systems

---

## 📦 Setup

1. **Clone the repo** (or copy files into a folder):

```bash
git clone https://github.com/taxx/jelly-cleaner.git
cd jelly-cleaner
```

2. **Create virtual environment** _(venv shown here)_: 

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install requirements**:
```bash
pip install -r requirements.txt
```

4. **Configuration** using config.yaml:
Create a `config.yaml` according to the `config.yaml.sample`.

## 🫙 Docker and Docker Compose
Clone the repo.
Create and adjust the `config.yaml` file based of the `config.yaml.sample`.
Adjust the `crontab` file to your liking
Start the docker container: `docker compose up -d`
_(Force rebuild: `docker compose down && docker compose build --no-cache && docker compose up -d`)_
Show the logs: `docker compose logs -n 10 -f`
