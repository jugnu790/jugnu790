import json
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

README = ROOT / "README.md"
DATA_FILE = ROOT / "data" / "processed.json"

USERNAME = os.getenv(
    "GITHUB_USERNAME",
    "jugnu790"
)


START_MARKER = "<!-- AUTO-GENERATED-START -->"
END_MARKER = "<!-- AUTO-GENERATED-END -->"


def load_data():
    with DATA_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def create_dynamic_section(data):
    profile = data["profile"]
    repos = data["repositories"]

    followers = profile.get(
        "followers",
        0
    )

    following = profile.get(
        "following",
        0
    )

    public_repos = profile.get(
        "public_repos",
        0
    )

    stars = repos.get(
        "stars",
        0
    )

    forks = repos.get(
        "forks",
        0
    )

    updated = datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d %H:%M UTC"
    )

    return f'''{START_MARKER}

## 📊 Live GitHub Statistics

<p align="center">

<img
src="./assets/stats-card.svg"
alt="GitHub statistics"
/>

</p>

| Metric | Value |
|---|---:|
| Repositories | {public_repos} |
| Stars | {stars} |
| Forks | {forks} |
| Followers | {followers} |
| Following | {following} |

---

## 🐍 Contribution Snake

<p align="center">

<img
src="./assets/github-contribution-grid-snake.svg"
alt="GitHub contribution snake"
/>

</p>

---

## 💻 Languages

<p align="center">

<img
src="./assets/languages-card.svg"
alt="Programming languages"
/>

</p>

---

## 🚀 Top Repositories

<p align="center">

<img
src="./assets/repositories-card.svg"
alt="Top repositories"
/>

</p>

---

### 🔄 Last automated update

`{updated}`

{END_MARKER}
'''


def update_readme():
    if README.exists():
        content = README.read_text(
            encoding="utf-8"
        )
    else:
        content = f"# {USERNAME}\n"

    new_section = create_dynamic_section(
        load_data()
    )

    start = content.find(
        START_MARKER
    )

    end = content.find(
        END_MARKER
    )

    if start != -1 and end != -1:
        end += len(END_MARKER)

        content = (
            content[:start]
            + new_section
            + content[end:]
        )

    else:
        if not content.endswith("\n"):
            content += "\n"

        content += "\n" + new_section

    README.write_text(
        content,
        encoding="utf-8"
    )

    print("README updated successfully.")


if __name__ == "__main__":
    update_readme()