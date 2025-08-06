import requests

class JellyseerClient:
    def __init__(self, api_url, api_key):
        self.base_url = api_url.rstrip("/")
        self.headers = {
            "accept": "application/json",
            "ApiKey": api_key
        }

    def get_requests(self):
        url = f"{self.base_url}/Request"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_requested_titles(self, whitelisted_users):
        raw_requests = self.get_requests()

        movie_titles = set()
        tv_titles = set()

        for r in raw_requests:
            user = r.get("requestedUser", {}).get("userAlias", "")
            title = r.get("title", "").strip().lower()
            media_type = r.get("mediaType")

            if user in whitelisted_users:
                continue  # Skip whitelisted

            if media_type == "movie":
                movie_titles.add(title)
            elif media_type == "tv":
                tv_titles.add(title)

        return movie_titles, tv_titles
