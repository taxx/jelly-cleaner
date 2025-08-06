import yaml
from jellyseer_client import JellyseerClient
from radarr_cleaner import RadarrCleaner
from sonarr_cleaner import SonarrCleaner

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()

    dry_run = config.get("dry_run", True)

    # Jellyseer
    jellyseer = JellyseerClient(
        config["jellyseer"]["api_url"],
        config["jellyseer"]["api_key"]
    )

    whitelisted_users = set(config.get("whitelisted_users", []))
    movie_titles, tv_titles = jellyseer.get_requested_titles(whitelisted_users)

    # Radarr
    radarr = RadarrCleaner(
        base_url=config["radarr"]["url"],
        api_key=config["radarr"]["api_key"],
        retention_days=config["retention_days"]["movies"],
        dry_run=dry_run
    )

    # Sonarr
    sonarr = SonarrCleaner(
        base_url=config["sonarr"]["url"],
        api_key=config["sonarr"]["api_key"],
        retention_days=config["retention_days"]["tv"],
        dry_run=dry_run
    )

    print("\n📦 Starting movie cleanup (Radarr)...")
    radarr.clean(movie_titles)

    print("\n📺 Starting TV show cleanup (Sonarr)...")
    sonarr.clean(tv_titles)

    print("\n✅ Cleanup finished.")

if __name__ == "__main__":
    main()
