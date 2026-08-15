import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests


USERNAME = os.getenv("GITHUB_USERNAME", "jugnu790")
TOKEN = os.getenv("GITHUB_TOKEN")

BASE_URL = "https://api.github.com"

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_headers():
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "jugnu790-github-profile"
    }

    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    return headers


HEADERS = get_headers()


def github_get(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=30
    )

    if response.status_code != 200:
        print(f"GitHub API error: {response.status_code}")
        print(response.text)
        response.raise_for_status()

    return response.json()


def fetch_profile():
    return github_get(f"/users/{USERNAME}")


def fetch_repositories():
    repositories = []

    page = 1

    while True:
        data = github_get(
            f"/users/{USERNAME}/repos",
            {
                "per_page": 100,
                "page": page,
                "sort": "updated",
                "direction": "desc"
            }
        )

        if not data:
            break

        repositories.extend(data)

        if len(data) < 100:
            break

        page += 1

    return repositories


def fetch_events():
    events = []
    page = 1

    while page <= 10:
        data = github_get(
            f"/users/{USERNAME}/events/public",
            {
                "per_page": 100,
                "page": page
            }
        )

        if not data:
            break

        events.extend(data)

        if len(data) < 100:
            break

        page += 1

    return events


def fetch_followers():
    return github_get(
        f"/users/{USERNAME}/followers",
        {
            "per_page": 100
        }
    )


def fetch_following():
    return github_get(
        f"/users/{USERNAME}/following",
        {
            "per_page": 100
        }
    )


def save_json(filename, data):
    path = DATA_DIR / filename

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"Saved {path}")


def main():
    print("=" * 60)
    print("GitHub Profile Data Fetcher")
    print("=" * 60)
    print(f"Username: {USERNAME}")

    profile = fetch_profile()
    repositories = fetch_repositories()
    events = fetch_events()

    try:
        followers = fetch_followers()
    except Exception as exc:
        print(f"Unable to fetch followers: {exc}")
        followers = []

    try:
        following = fetch_following()
    except Exception as exc:
        print(f"Unable to fetch following: {exc}")
        following = []

    metadata = {
        "username": USERNAME,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "source": "GitHub API"
    }

    save_json("profile.json", profile)
    save_json("repositories.json", repositories)
    save_json("events.json", events)
    save_json("followers.json", followers)
    save_json("following.json", following)
    save_json("metadata.json", metadata)

    print()
    print("Data fetching completed successfully.")
    print(f"Repositories: {len(repositories)}")
    print(f"Events: {len(events)}")
    print(f"Followers returned: {len(followers)}")
    print(f"Following returned: {len(following)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted.")
        sys.exit(130)
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)