import requests
from datetime import datetime, timezone
from dateutil.parser import isoparse

class RadarrCleaner:
    def __init__(self, base_url, api_key, retention_days, dry_run):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.retention_days = retention_days
        self.dry_run = dry_run
        self.headers = {"X-Api-Key": api_key}

    def get_movies(self):
        url = f"{self.base_url}/api/v3/movie"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def delete_movie(self, movie_id, title):
        url = f"{self.base_url}/api/v3/movie/{movie_id}?deleteFiles=true&addExclusion=false"
        if self.dry_run:
            print(f"[DRY RUN] Skulle ha tagit bort film: {title}")
        else:
            response = requests.delete(url, headers=self.headers)
            if response.status_code == 200:
                print(f"[OK] Tog bort film: {title}")
            else:
                print(f"[FEL] Kunde inte ta bort {title}: {response.status_code} {response.text}")

    def is_older_than_retention(self, iso_date):
        try:
            dt = isoparse(iso_date)
            now = datetime.now(timezone.utc)
            age_days = (now - dt).days
            return age_days >= self.retention_days
        except Exception as e:
            print(f"Fel vid datumtolkning: {e}")
            return False

    def clean(self, allowed_titles):
        movies = self.get_movies()

        for movie in movies:
            title = movie["title"].strip().lower()
            movie_id = movie["id"]
            movie_file = movie.get("movieFile")

            if not movie_file:
                continue  # Film ej nedladdad

            if title not in allowed_titles:
                continue  # Inte begärt av någon (eller whitelisted)

            added_date = movie_file.get("dateAdded")
            if not added_date:
                continue

            if self.is_older_than_retention(added_date):
                self.delete_movie(movie_id, title)
