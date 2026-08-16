import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests


# ============================================================
# CONFIGURATION
# ============================================================

USERNAME = os.getenv("GITHUB_USERNAME", "jugnu790")

# PROFILE_GITHUB_TOKEN is preferred because a personal token can
# provide better access to the authenticated user's contribution
# information.
#
# If it is not configured, fall back to GitHub Actions'
# automatically provided GITHUB_TOKEN.
TOKEN = (
    os.getenv("PROFILE_GITHUB_TOKEN")
    or os.getenv("GITHUB_TOKEN")
)

BASE_URL = "https://api.github.com"
GRAPHQL_URL = "https://api.github.com/graphql"

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

REQUEST_TIMEOUT = 30

API_VERSION = "2022-11-28"


# ============================================================
# HTTP HEADERS
# ============================================================

def get_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "jugnu790-github-profile-automation",
    }

    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    return headers


HEADERS = get_headers()


# ============================================================
# GENERIC REST REQUEST
# ============================================================

def github_get(
    endpoint: str,
    params: dict[str, Any] | None = None,
) -> Any:
    """
    Perform a GET request against the GitHub REST API.

    Raises an exception when GitHub returns an error.
    """

    url = f"{BASE_URL}{endpoint}"

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=REQUEST_TIMEOUT,
    )

    if response.status_code != 200:
        print()
        print("=" * 70)
        print("GitHub REST API ERROR")
        print("=" * 70)
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        print(response.text[:2000])
        print("=" * 70)
        print()

        response.raise_for_status()

    return response.json()


# ============================================================
# GRAPHQL REQUEST
# ============================================================

def github_graphql(
    query: str,
    variables: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute a GitHub GraphQL query.
    """

    if not TOKEN:
        raise RuntimeError(
            "No GitHub token is available. "
            "Set GITHUB_TOKEN or PROFILE_GITHUB_TOKEN."
        )

    response = requests.post(
        GRAPHQL_URL,
        headers=HEADERS,
        json={
            "query": query,
            "variables": variables,
        },
        timeout=REQUEST_TIMEOUT,
    )

    if response.status_code != 200:
        print()
        print("=" * 70)
        print("GitHub GRAPHQL HTTP ERROR")
        print("=" * 70)
        print(f"Status: {response.status_code}")
        print(response.text[:2000])
        print("=" * 70)
        print()

        response.raise_for_status()

    payload = response.json()

    if payload.get("errors"):
        print()
        print("=" * 70)
        print("GitHub GRAPHQL API ERROR")
        print("=" * 70)

        for error in payload["errors"]:
            print(error)

        print("=" * 70)
        print()

        raise RuntimeError(
            "GitHub GraphQL returned one or more errors."
        )

    return payload["data"]


# ============================================================
# PROFILE
# ============================================================

def fetch_profile() -> dict[str, Any]:
    print("Fetching profile...")

    return github_get(
        f"/users/{USERNAME}"
    )


# ============================================================
# REPOSITORIES
# ============================================================

def fetch_repositories() -> list[dict[str, Any]]:
    print("Fetching repositories...")

    repositories: list[dict[str, Any]] = []

    page = 1

    while True:
        data = github_get(
            f"/users/{USERNAME}/repos",
            {
                "per_page": 100,
                "page": page,
                "sort": "updated",
                "direction": "desc",
            },
        )

        if not data:
            break

        repositories.extend(data)

        print(
            f"  repositories page {page}: "
            f"{len(data)}"
        )

        if len(data) < 100:
            break

        page += 1

    return repositories


# ============================================================
# PUBLIC EVENTS
# ============================================================

def fetch_events() -> list[dict[str, Any]]:
    """
    Fetch public GitHub events.

    GitHub limits this endpoint to recent public activity.
    Therefore events are NOT used as the authoritative source
    for the contribution calendar.
    """

    print("Fetching public events...")

    events: list[dict[str, Any]] = []

    page = 1

    # GitHub's public-events endpoint has a limited history.
    # Ten pages is enough for our recent activity dashboard.
    while page <= 10:

        data = github_get(
            f"/users/{USERNAME}/events/public",
            {
                "per_page": 100,
                "page": page,
            },
        )

        if not data:
            break

        events.extend(data)

        print(
            f"  events page {page}: "
            f"{len(data)}"
        )

        if len(data) < 100:
            break

        page += 1

    return events


# ============================================================
# FOLLOWERS
# ============================================================

def fetch_followers() -> list[dict[str, Any]]:
    print("Fetching followers...")

    followers: list[dict[str, Any]] = []

    page = 1

    while True:

        data = github_get(
            f"/users/{USERNAME}/followers",
            {
                "per_page": 100,
                "page": page,
            },
        )

        if not data:
            break

        followers.extend(data)

        if len(data) < 100:
            break

        page += 1

    return followers


# ============================================================
# FOLLOWING
# ============================================================

def fetch_following() -> list[dict[str, Any]]:
    print("Fetching following...")

    following: list[dict[str, Any]] = []

    page = 1

    while True:

        data = github_get(
            f"/users/{USERNAME}/following",
            {
                "per_page": 100,
                "page": page,
            },
        )

        if not data:
            break

        following.extend(data)

        if len(data) < 100:
            break

        page += 1

    return following


# ============================================================
# STARRED REPOSITORIES
# ============================================================

def fetch_starred_repositories() -> list[dict[str, Any]]:
    """
    Fetch repositories starred by the user.

    This is separate from repositories owned by the user.
    """

    print("Fetching starred repositories...")

    starred: list[dict[str, Any]] = []

    page = 1

    while True:

        data = github_get(
            f"/users/{USERNAME}/starred",
            {
                "per_page": 100,
                "page": page,
            },
        )

        if not data:
            break

        starred.extend(data)

        if len(data) < 100:
            break

        page += 1

    return starred


# ============================================================
# CONTRIBUTION GRAPHQL QUERY
# ============================================================

CONTRIBUTIONS_QUERY = """
query(
    $login: String!,
    $from: DateTime!,
    $to: DateTime!
) {
    user(login: $login) {
        login
        name
        contributionsCollection(
            from: $from,
            to: $to
        ) {
            startedAt
            endedAt

            totalCommitContributions
            restrictedContributionsCount

            commitContributionsByRepository {
                repository {
                    name
                    nameWithOwner
                    url
                    primaryLanguage {
                        name
                    }
                }
                contributions {
                    totalCount
                }
            }

            issueContributions {
                totalCount
            }

            pullRequestContributions {
                totalCount
            }

            pullRequestReviewContributions {
                totalCount
            }

            repositoryContributions {
                totalCount
            }

            issueContributionsByRepository(
                first: 100
            ) {
                totalCount
            }

            pullRequestContributionsByRepository(
                first: 100
            ) {
                totalCount
            }

            pullRequestReviewContributionsByRepository(
                first: 100
            ) {
                totalCount
            }

            repositoryContributionsByRepository(
                first: 100
            ) {
                totalCount
            }

            contributionCalendar {
                totalContributions

                weeks {
                    contributionDays {
                        date
                        contributionCount
                        weekday
                        color
                    }
                }
            }
        }
    }
}
"""


# ============================================================
# CONTRIBUTIONS
# ============================================================

def fetch_contributions() -> dict[str, Any]:
    """
    Fetch the authenticated user's contribution calendar and
    contribution categories.

    The GitHub contribution calendar is the authoritative source
    for the contribution heatmap.

    The range covers approximately the previous 365 days.
    """

    print("Fetching contribution calendar...")

    now = datetime.now(timezone.utc)

    start = now - timedelta(days=365)

    variables = {
        "login": USERNAME,
        "from": start.isoformat(),
        "to": now.isoformat(),
    }

    try:

        data = github_graphql(
            CONTRIBUTIONS_QUERY,
            variables,
        )

        user = data.get("user")

        if not user:
            raise RuntimeError(
                f"GitHub GraphQL could not find user "
                f"'{USERNAME}'."
            )

        collection = user.get(
            "contributionsCollection",
            {},
        )

        print(
            "Contribution calendar fetched successfully."
        )

        return {
            "username": USERNAME,
            "range": {
                "from": start.isoformat(),
                "to": now.isoformat(),
            },
            "collection": collection,
        }

    except Exception as exc:

        print()
        print(
            "WARNING: Contribution GraphQL request failed."
        )
        print(f"Reason: {exc}")
        print()
        print(
            "The workflow will continue using the REST "
            "data that is available."
        )
        print()

        return {
            "username": USERNAME,
            "range": {
                "from": start.isoformat(),
                "to": now.isoformat(),
            },
            "collection": {},
            "error": str(exc),
        }


# ============================================================
# SAVE JSON
# ============================================================

def save_json(
    filename: str,
    data: Any,
) -> None:

    path = DATA_DIR / filename

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Saved: {path.relative_to(ROOT)}"
    )


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print()
    print("=" * 70)
    print("GitHub Profile Data Fetcher")
    print("=" * 70)
    print(f"Username: {USERNAME}")
    print(
        f"Token available: {'yes' if TOKEN else 'no'}"
    )
    print("=" * 70)
    print()

    # --------------------------------------------------------
    # Main GitHub data
    # --------------------------------------------------------

    profile = fetch_profile()

    repositories = fetch_repositories()

    events = fetch_events()

    # --------------------------------------------------------
    # Social data
    # --------------------------------------------------------

    try:
        followers = fetch_followers()
    except Exception as exc:
        print(
            f"WARNING: Could not fetch followers: {exc}"
        )
        followers = []

    try:
        following = fetch_following()
    except Exception as exc:
        print(
            f"WARNING: Could not fetch following: {exc}"
        )
        following = []

    try:
        starred = fetch_starred_repositories()
    except Exception as exc:
        print(
            f"WARNING: Could not fetch starred repositories: "
            f"{exc}"
        )
        starred = []

    # --------------------------------------------------------
    # Contribution data
    # --------------------------------------------------------

    contributions = fetch_contributions()

    # --------------------------------------------------------
    # Metadata
    # --------------------------------------------------------

    metadata = {
        "username": USERNAME,
        "updated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "source": [
            "GitHub REST API",
            "GitHub GraphQL API",
        ],
        "api_version": API_VERSION,
        "data_description": {
            "profile": True,
            "repositories": True,
            "events": True,
            "followers": True,
            "following": True,
            "starred_repositories": True,
            "contributions": True,
        },
    }

    # --------------------------------------------------------
    # Save everything
    # --------------------------------------------------------

    save_json(
        "profile.json",
        profile,
    )

    save_json(
        "repositories.json",
        repositories,
    )

    save_json(
        "events.json",
        events,
    )

    save_json(
        "followers.json",
        followers,
    )

    save_json(
        "following.json",
        following,
    )

    save_json(
        "starred.json",
        starred,
    )

    save_json(
        "contributions.json",
        contributions,
    )

    save_json(
        "metadata.json",
        metadata,
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    collection = contributions.get(
        "collection",
        {},
    )

    calendar = collection.get(
        "contributionCalendar",
        {},
    )

    print()
    print("=" * 70)
    print("FETCH COMPLETE")
    print("=" * 70)
    print(
        f"Repositories: "
        f"{len(repositories)}"
    )
    print(
        f"Public events fetched: "
        f"{len(events)}"
    )
    print(
        f"Followers fetched: "
        f"{len(followers)}"
    )
    print(
        f"Following fetched: "
        f"{len(following)}"
    )
    print(
        f"Starred repositories: "
        f"{len(starred)}"
    )
    print(
        f"Contribution total: "
        f"{calendar.get('totalContributions', 0)}"
    )
    print(
        f"Commit contributions: "
        f"{collection.get('totalCommitContributions', 0)}"
    )
    print(
        f"Issue contributions: "
        f"{collection.get('issueContributions', {}).get('totalCount', 0)}"
    )
    print(
        f"Pull requests: "
        f"{collection.get('pullRequestContributions', {}).get('totalCount', 0)}"
    )
    print(
        f"PR reviews: "
        f"{collection.get('pullRequestReviewContributions', {}).get('totalCount', 0)}"
    )
    print("=" * 70)
    print()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:

        print(
            "Interrupted by user."
        )

        sys.exit(130)

    except Exception as exc:

        print()
        print("=" * 70)
        print("FATAL ERROR")
        print("=" * 70)
        print(exc)
        print("=" * 70)
        print()

        sys.exit(1)