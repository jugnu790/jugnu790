import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"

ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    with (DATA_DIR / "processed.json").open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def escape(value):
    if value is None:
        return ""

    return html.escape(str(value))


def write_file(path, content):
    with path.open("w", encoding="utf-8") as file:
        file.write(content)

    print(f"Generated: {path}")


def build_stats_card(data):
    profile = data["profile"]
    repos = data["repositories"]
    events = data["events"]

    username = escape(
        profile.get("login") or "jugnu790"
    )

    name = escape(
        profile.get("name") or username
    )

    followers = profile.get("followers", 0)
    following = profile.get("following", 0)
    public_repos = profile.get("public_repos", 0)
    stars = repos.get("stars", 0)
    forks = repos.get("forks", 0)
    event_count = events.get("total", 0)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="500"
height="260"
viewBox="0 0 500 260">

<rect
x="0"
y="0"
width="500"
height="260"
rx="16"
fill="#0d1117"
stroke="#30363d"/>

<text
x="28"
y="38"
fill="#f0f6fc"
font-size="22"
font-family="Arial, Helvetica, sans-serif"
font-weight="700">
{name}
</text>

<text
x="28"
y="62"
fill="#8b949e"
font-size="14"
font-family="Arial, Helvetica, sans-serif">
@{username}
</text>

<text x="30" y="105"
fill="#8b949e"
font-size="13"
font-family="Arial">
Repositories
</text>

<text x="30" y="130"
fill="#f0f6fc"
font-size="22"
font-family="Arial"
font-weight="700">
{public_repos}
</text>

<text x="180" y="105"
fill="#8b949e"
font-size="13"
font-family="Arial">
Stars
</text>

<text x="180" y="130"
fill="#f0f6fc"
font-size="22"
font-family="Arial"
font-weight="700">
{stars}
</text>

<text x="330" y="105"
fill="#8b949e"
font-size="13"
font-family="Arial">
Forks
</text>

<text x="330" y="130"
fill="#f0f6fc"
font-size="22"
font-family="Arial"
font-weight="700">
{forks}
</text>

<text x="30" y="175"
fill="#8b949e"
font-size="13"
font-family="Arial">
Followers
</text>

<text x="30" y="200"
fill="#f0f6fc"
font-size="22"
font-family="Arial"
font-weight="700">
{followers}
</text>

<text x="180" y="175"
fill="#8b949e"
font-size="13"
font-family="Arial">
Following
</text>

<text x="180" y="200"
fill="#f0f6fc"
font-size="22"
font-family="Arial"
font-weight="700">
{following}
</text>

<text x="330" y="175"
fill="#8b949e"
font-size="13"
font-family="Arial">
Recent events
</text>

<text x="330" y="200"
fill="#f0f6fc"
font-size="22"
font-family="Arial"
font-weight="700">
{event_count}
</text>

<text
x="28"
y="238"
fill="#8b949e"
font-size="11"
font-family="Arial">
Automatically updated by GitHub Actions
</text>

</svg>
'''

    write_file(
        ASSETS_DIR / "stats-card.svg",
        svg
    )


def build_languages_card(data):
    languages = data.get("languages", {})

    total = sum(languages.values())

    rows = []

    y = 40

    for language, count in list(languages.items())[:8]:

        percentage = (
            (count / total) * 100
            if total
            else 0
        )

        rows.append(
            f'''
<text
x="24"
y="{y}"
fill="#f0f6fc"
font-size="13"
font-family="Arial">
{escape(language)}
</text>

<text
x="430"
y="{y}"
fill="#8b949e"
font-size="13"
font-family="Arial"
text-anchor="end">
{percentage:.1f}%
</text>
'''
        )

        y += 32

    height = max(
        100,
        25 + len(rows) * 32
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="460"
height="{height}"
viewBox="0 0 460 {height}">

<rect
width="460"
height="{height}"
rx="16"
fill="#0d1117"
stroke="#30363d"/>

<text
x="24"
y="22"
fill="#f0f6fc"
font-size="15"
font-family="Arial"
font-weight="700">
Languages
</text>

{''.join(rows)}

</svg>
'''

    write_file(
        ASSETS_DIR / "languages-card.svg",
        svg
    )


def build_repositories_card(data):
    repositories = data.get(
        "top_repositories",
        []
    )

    rows = []

    y = 30

    for repo in repositories[:6]:

        name = escape(
            repo.get("name", "")
        )

        stars = repo.get(
            "stars",
            0
        )

        language = escape(
            repo.get("language") or "Unknown"
        )

        rows.append(
            f'''
<text
x="20"
y="{y}"
fill="#58a6ff"
font-size="13"
font-family="Arial"
font-weight="700">
{name}
</text>

<text
x="330"
y="{y}"
fill="#8b949e"
font-size="12"
font-family="Arial">
★ {stars}
</text>

<text
x="20"
y="{y + 17}"
fill="#8b949e"
font-size="11"
font-family="Arial">
{language}
</text>
'''
        )

        y += 52

    height = max(
        100,
        25 + len(rows) * 52
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="460"
height="{height}"
viewBox="0 0 460 {height}">

<rect
width="460"
height="{height}"
rx="16"
fill="#0d1117"
stroke="#30363d"/>

<text
x="20"
y="18"
fill="#f0f6fc"
font-size="15"
font-family="Arial"
font-weight="700">
Top repositories
</text>

{''.join(rows)}

</svg>
'''

    write_file(
        ASSETS_DIR / "repositories-card.svg",
        svg
    )


def main():
    data = load_data()

    build_stats_card(data)
    build_languages_card(data)
    build_repositories_card(data)

    print("All cards generated.")


if __name__ == "__main__":
    main()