import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def load_json(filename, default=None):
    path = DATA_DIR / filename

    if not path.exists():
        return default if default is not None else {}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def calculate_repository_stats(repositories):
    total = len(repositories)

    public = sum(
        1 for repo in repositories
        if not repo.get("private", False)
    )

    forks = sum(
        repo.get("forks_count", 0)
        for repo in repositories
    )

    stars = sum(
        repo.get("stargazers_count", 0)
        for repo in repositories
    )

    open_issues = sum(
        repo.get("open_issues_count", 0)
        for repo in repositories
    )

    archived = sum(
        1 for repo in repositories
        if repo.get("archived", False)
    )

    return {
        "total": total,
        "public": public,
        "forks": forks,
        "stars": stars,
        "open_issues": open_issues,
        "archived": archived
    }


def calculate_languages(repositories):
    counter = Counter()

    for repo in repositories:
        language = repo.get("language")

        if language:
            counter[language] += 1

    return dict(
        counter.most_common()
    )


def calculate_top_repositories(repositories):
    repositories = sorted(
        repositories,
        key=lambda repo: (
            repo.get("stargazers_count", 0),
            repo.get("forks_count", 0)
        ),
        reverse=True
    )

    result = []

    for repo in repositories[:10]:
        result.append({
            "name": repo.get("name"),
            "full_name": repo.get("full_name"),
            "description": repo.get("description"),
            "html_url": repo.get("html_url"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language"),
            "updated_at": repo.get("updated_at")
        })

    return result


def calculate_event_stats(events):
    counter = Counter()

    for event in events:
        event_type = event.get("type")

        if event_type:
            counter[event_type] += 1

    return dict(
        counter.most_common()
    )


def main():
    profile = load_json("profile.json", {})
    repositories = load_json("repositories.json", [])
    events = load_json("events.json", [])

    repository_stats = calculate_repository_stats(
        repositories
    )

    languages = calculate_languages(
        repositories
    )

    top_repositories = calculate_top_repositories(
        repositories
    )

    event_stats = calculate_event_stats(
        events
    )

    processed = {
        "profile": {
            "login": profile.get("login"),
            "name": profile.get("name"),
            "bio": profile.get("bio"),
            "company": profile.get("company"),
            "location": profile.get("location"),
            "blog": profile.get("blog"),
            "public_repos": profile.get("public_repos", 0),
            "public_gists": profile.get("public_gists", 0),
            "followers": profile.get("followers", 0),
            "following": profile.get("following", 0),
            "created_at": profile.get("created_at"),
            "updated_at": profile.get("updated_at")
        },

        "repositories": repository_stats,

        "languages": languages,

        "top_repositories": top_repositories,

        "events": {
            "total": len(events),
            "types": event_stats
        }
    }

    output = DATA_DIR / "processed.json"

    with output.open("w", encoding="utf-8") as file:
        json.dump(
            processed,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"Generated: {output}")


if __name__ == "__main__":
    main()