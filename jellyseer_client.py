import requests

class JellyseerClient:
    def __init__(self, base_url, email, password):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.email = email
        self.password = password
        self.authenticated = False

    def login(self):
        url = f"{self.base_url}/auth/local"
        payload = {"email": self.email, "password": self.password}
        response = self.session.post(url, json=payload)
        if response.status_code == 200:
            self.authenticated = True
            print("🔐 Jellyseer login successful")
        else:
            raise Exception(f"Login failed: {response.status_code} {response.text}")

    def get_requests(self):
        if not self.authenticated:
            self.login()
        url = f"{self.base_url}/Request?take=1000&skip=0&filter=available&sort=added&sortDirection=desc&mediaType=all"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("results", [])

    def get_media_title(self, slug_id, media_type):
        if not self.authenticated:
            self.login()
        url = f"{self.base_url}/{media_type}/{slug_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("originalTitle", "unknown title")

    def get_old_requests(self, cutoff_datetime):
        print("cutoff_datetime:", cutoff_datetime)
        raw_requests = self.get_requests()
        deletions = []

        # Remove duplicates by media ID, and keep the one with the most recent createdAt date
        unique_requests = {}
        for request in raw_requests:
            media = request.get("media")
            if not media:
                continue
            media_id = media.get("id")
            created_at = request.get("createdAt")
            if not media_id or not created_at:
                continue
            # If this media_id is not seen yet, or this request is newer, keep it
            if (media_id not in unique_requests) or (created_at > unique_requests[media_id].get("createdAt", "")):
                unique_requests[media_id] = request
        filtered_requests = list(unique_requests.values())

        for request in filtered_requests:
            requested_by = request.get("requestedBy", {})
            username = (
                requested_by.get("jellyfinUsername")
                or requested_by.get("displayName")
                or ""
            ).lower()

            created_at = request.get("createdAt")
            if not created_at or created_at > cutoff_datetime.isoformat():
                continue

            media = request.get("media")
            if not media:
                continue

            media_id = media.get("id")
            title = self.get_media_title(media.get("externalServiceSlug"), media.get("mediaType"))
            request_id = request.get("id")
            deletions.append((media_id, title, created_at, request_id, username))

        return deletions

    def delete_media(self, media_id):
        if not self.authenticated:
            self.login()

        headers = {"accept": "*/*"}

        # Step 1: delete media files
        file_url = f"{self.base_url}/api/v1/media/{media_id}/file"
        file_resp = self.session.delete(file_url, headers=headers)
        if file_resp.status_code == 204:
            print(f"🗑️  Deleted files for media ID {media_id}")
        elif file_resp.status_code == 404:
            print(f"⚠️  Files not found for media ID {media_id} (might already be gone)")
        else:
            print(f"❌ Failed to delete files: {file_resp.status_code} {file_resp.text}")

        # Step 2: delete media metadata
        meta_url = f"{self.base_url}/api/v1/media/{media_id}"
        meta_resp = self.session.delete(meta_url, headers=headers)
        if meta_resp.status_code == 204:
            print(f"🧹 Deleted metadata for media ID {media_id}")
        elif meta_resp.status_code == 404:
            print(f"⚠️  Metadata not found for media ID {media_id}")
        else:
            print(f"❌ Failed to delete metadata: {meta_resp.status_code} {meta_resp.text}")
