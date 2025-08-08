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
    retention_days = int(retention_cfg.get("all", 60))

    now = datetime.now()
    cutoff_date = now - timedelta(days=retention_days)
 
    deletions = jellyseer.get_old_requests(
        cutoff_datetime=cutoff_date
    )

    print(f"🧹 Found {len(deletions)} media items to delete")


    for media_id, title, created_at, request_id, username in deletions:
        if username in whitelisted_users:
            #print(f"Skipping whitelisted user: {username}")
            print(f"🙈  Skipping to delete request from {username}: {title} (ID: {media_id}), Created at: {created_at}, Request ID: {request_id}")

            continue

        print(f"🗑️  Would delete: {title} (ID: {media_id}), Created at: {created_at}, Request ID: {request_id}, Requested by: {username})")
        if not dry_run:
            jellyseer.delete_media(media_id)

if __name__ == "__main__":
    main()
