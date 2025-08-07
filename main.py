import yaml
from datetime import datetime, timedelta
from jellyseer_client import JellyseerClient

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()

    whitelisted_users = set(user.lower() for user in config.get("whitelist", []))
    dry_run = config.get("dry_run", True)

    jellyseer_cfg = config.get("jellyseer", {})
    jellyseer = JellyseerClient(
        base_url=jellyseer_cfg["api_url"],
        email=jellyseer_cfg["email"],
        password=jellyseer_cfg["password"]
    )

    retention_cfg = config.get("retention_days", {})
    retention_movies = int(retention_cfg.get("movies", 60))
    retention_tv = int(retention_cfg.get("tv", 60))

    now = datetime.now()
    cutoff_movies = now - timedelta(days=retention_movies)
    cutoff_tv = now - timedelta(days=retention_tv)

    deletions = jellyseer.get_old_requests(
        whitelisted_users=whitelisted_users,
        cutoff_datetime=min(cutoff_movies, cutoff_tv)
    )

    print(f"🧹 Found {len(deletions)} media items to delete")

    for media_id, title in deletions:
        print(f"🗑️  Would delete: {title} (ID: {media_id})")
        if not dry_run:
            jellyseer.delete_media(media_id)

if __name__ == "__main__":
    main()
