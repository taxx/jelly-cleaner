import requests
from datetime import datetime, timezone
from dateutil.parser import isoparse

class SonarrCleaner:
    def __init__(self, base_url, api_key, retention_days, dry_run):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.retention_days = retention_days
        self.dry_run = dry_run
        self.headers = {"X-Api-Key": api_key}

    def get_series(self):
        url = f"{self.base_url}/api/v3/series"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def delete_series(self, series_id, title):
        url = f"{self.base_url}/api/v3/series/{series_id}?deleteFiles=true&addExclusion=false"
        if self.dry_run:
            print(f"[DRY RUN] Would delete TV series: {title}")
        else:
            response = requests.delete(url, headers=self.headers)
            if response.status_code == 200:
                print(f"[OK] Deleted TV series: {title}")
            else:
                print(f"[ERROR] Could not delete {title}: {response.status_code} {response.text}")

    def is_older_than_retention(self, iso_date):
        try:
            dt = isoparse(iso_date)
            now = datetime.now(timezone.utc)
            age_days = (now - dt).days
            return age_days >= self.retention_days
        except Exception as e:
            print(f"Date parse error: {e}")
            return False

    def clean(self, allowed_titles):
        series_list = self.get_series()

        for series in series_list:
            title = series["title"].strip().lower()
            series_id = series["id"]

            stats = series.get("statistics")
            if not stats or not stats.get("episodeFileCount", 0):
                continue  # Skip empty or unmonitored series

            last_file_date = stats.get("lastEpisodeFileDate")
            if not last_file_date:
                continue

            if title not in allowed_titles:
                continue

            if self.is_older_than_retention(last_file_date):
                self.delete_series(series_id, title)
