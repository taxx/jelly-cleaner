# Jellyseer Media Cleaner

This Python tool automatically deletes old movies and TV shows that were previously requested through Jellyseer, using the Radarr and Sonarr APIs.

It's useful for home media servers with limited space and supports:
- Separate retention periods for movies and TV shows
- Per-user whitelisting (media is never deleted if requested by whitelisted users)
- Dry-run mode (safe preview of what would be deleted)

---

## 🚀 Features

- Deletes entire **movies via Radarr**
- Deletes entire **TV shows via Sonarr**
- Skips requests by **whitelisted users**
- Uses **Jellyseer API** to track who requested what
- Supports **dry-run** mode (no actual deletion)

---

## 🛠️ Requirements

- Python 3.8+
- Access to your Jellyseer, Sonarr, and Radarr APIs
- API keys for all three systems

---

## 📦 Setup

1. **Clone the repo** (or copy files into a folder):

```bash
git clone https://github.com/yourname/jellyseer-media-cleaner.git
cd jellyseer-media-cleaner

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

Create a `config.yaml` according to the `config.yaml.sample`.

