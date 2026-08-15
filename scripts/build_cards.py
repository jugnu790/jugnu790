#!/usr/bin/env python3
"""
Builds themed, animated GitHub cards into assets/ so the profile README never
depends on a third-party rendering service.

Usage:
    GH_TOKEN=xxx python scripts/build_cards.py jugnu790
    python scripts/build_cards.py jugnu790 --mock      # layout preview, no network
"""

import json
import os
import sys
import urllib.request
from datetime import date, datetime

# ---------------------------------------------------------------- theme
BG_A, BG_B = "#020617", "#06182A"
LINE = "#0E7490"
DIM = "#475569"
TEXT = "#CBD5E1"
BRIGHT = "#F8FAFC"
CYAN = "#22D3EE"
TEAL = "#0F766E"
AMBER = "#F59E0B"
GREEN = "#4ADE80"
MONO = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, monospace"

HEAT = ["#0B1220", "#0E4A55", "#0891B2", "#22D3EE", "#A5F3FC"]

QUERY = """
query($login:String!) {
  user(login:$login) {
    login
    followers { totalCount }
    repositories(first:100, ownerAffiliations:OWNER, isFork:false,
                 orderBy:{field:STARGAZERS, direction:DESC}) {
      totalCount
      nodes {
        stargazerCount
        languages(first:10, orderBy:{field:SIZE, direction:DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={
            "Authorization": "bearer " + token,
            "Content-Type": "application/json",
            "User-Agent": "profile-card-builder",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise SystemExit("GitHub API error: " + json.dumps(payload["errors"]))
    return payload["data"]["user"]


def mock_user():
    import random

    random.seed(7)
    weeks = []
    for w in range(53):
        days = []
        for d in range(7):
            n = 0 if random.random() < 0.55 else random.randint(1, 14)
            days.append({"date": "2026-01-01", "contributionCount": n})
        weeks.append({"contributionDays": days})
    return {
        "login": "jugnu790",
        "followers": {"totalCount": 41},
        "repositories": {
            "totalCount": 38,
            "nodes": [
                {"stargazerCount": 6, "languages": {"edges": [
                    {"size": 480000, "node": {"name": "Java", "color": "#b07219"}},
                    {"size": 120000, "node": {"name": "JavaScript", "color": "#f1e05a"}}]}},
                {"stargazerCount": 3, "languages": {"edges": [
                    {"size": 220000, "node": {"name": "JavaScript", "color": "#f1e05a"}},
                    {"size": 90000, "node": {"name": "CSS", "color": "#563d7c"}},
                    {"size": 60000, "node": {"name": "HTML", "color": "#e34c26"}}]}},
                {"stargazerCount": 1, "languages": {"edges": [
                    {"size": 70000, "node": {"name": "Python", "color": "#3572A5"}},
                    {"size": 30000, "node": {"name": "Shell", "color": "#89e051"}}]}},
            ],
        },
        "contributionsCollection": {
            "totalCommitContributions": 812,
            "totalPullRequestContributions": 64,
            "totalIssueContributions": 23,
            "totalPullRequestReviewContributions": 37,
            "restrictedContributionsCount": 138,
            "contributionCalendar": {"totalContributions": 1074, "weeks": weeks},
        },
    }


# ---------------------------------------------------------------- derive
def digest(u):
    cc = u["contributionsCollection"]
    cal = cc["contributionCalendar"]
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]

    stars = sum(r["stargazerCount"] for r in u["repositories"]["nodes"])

    langs = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            n = e["node"]["name"]
            if n not in langs:
                langs[n] = {"size": 0, "color": e["node"]["color"] or CYAN}
            langs[n]["size"] += e["size"]
    top = sorted(langs.items(), key=lambda kv: -kv[1]["size"])[:8]
    total_size = sum(v["size"] for _, v in top) or 1

    # streaks
    longest = cur = run = 0
    for d in days:
        if d["contributionCount"] > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    for d in reversed(days):
        if d["contributionCount"] > 0:
            cur += 1
        elif cur == 0:
            continue  # today may still be empty
        else:
            break

    best = max((d["contributionCount"] for d in days), default=0)
    active = sum(1 for d in days if d["contributionCount"] > 0)

    return {
        "login": u["login"],
        "weeks": weeks,
        "total": cal["totalContributions"],
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "issues": cc["totalIssueContributions"],
        "reviews": cc["totalPullRequestReviewContributions"],
        "private": cc["restrictedContributionsCount"],
        "stars": stars,
        "followers": u["followers"]["totalCount"],
        "repos": u["repositories"]["totalCount"],
        "langs": [(n, v["size"] / total_size, v["color"]) for n, v in top],
        "lang_count": len(langs),
        "current_streak": cur,
        "longest_streak": longest,
        "best_day": best,
        "active_days": active,
    }


MOCK = False


def shell(w, h, title, sub=""):
    if MOCK:
        sub = "sample data - run the cards workflow"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{BG_A}"/><stop offset="100%" stop-color="{BG_B}"/>
  </linearGradient>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{TEAL}"/><stop offset="60%" stop-color="{CYAN}"/><stop offset="100%" stop-color="{AMBER}"/>
  </linearGradient>
  <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.45"/>
    <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="{w}" height="{h}" rx="14" fill="url(#bg)" stroke="{LINE}" stroke-opacity="0.5"/>
<text x="24" y="34" fill="{CYAN}" font-size="13" letter-spacing="4" font-family="{MONO}">{esc(title)}</text>
<text x="{w-24}" y="34" fill="{DIM}" font-size="11" text-anchor="end" font-family="{MONO}">{esc(sub)}</text>
<rect x="24" y="46" width="{w-48}" height="1" fill="{LINE}" opacity="0.4"/>
"""


# ---------------------------------------------------------------- cards
def card_stats(d, path):
    W, H = 500, 320
    p = [shell(W, H, "CONTRIBUTION STATS", "last 12 months")]

    # ring
    cx, cy, r = 118, 178, 62
    circ = 2 * 3.14159 * r
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#0B1220" stroke-width="12"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#accent)" stroke-width="12" '
             f'stroke-linecap="round" transform="rotate(-90 {cx} {cy})" '
             f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ*0.18:.1f}">'
             f'<animate attributeName="stroke-dashoffset" values="{circ:.1f};{circ*0.18:.1f};{circ*0.18:.1f}" '
             f'keyTimes="0;0.45;1" dur="8s" repeatCount="indefinite"/></circle>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{CYAN}" stroke-opacity="0.5">'
             f'<animate attributeName="r" values="{r};{r+22}" dur="3.4s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0.5;0" dur="3.4s" repeatCount="indefinite"/></circle>')
    p.append(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" fill="{BRIGHT}" font-size="30" font-weight="700" '
             f'font-family="{MONO}">{d["total"]}</text>')
    p.append(f'<text x="{cx}" y="{cy+86}" text-anchor="middle" fill="{DIM}" font-size="10" letter-spacing="1.5" '
             f'font-family="{MONO}">CONTRIBUTIONS</text>')
    p.append(f'<text x="{cx}" y="{cy+108}" text-anchor="middle" fill="{GREEN}" font-size="11" '
             f'font-family="{MONO}">{d["active_days"]} active days</text>')

    rows = [
        ("Commits", d["commits"], AMBER),
        ("Pull requests", d["prs"], CYAN),
        ("Code reviews", d["reviews"], GREEN),
        ("Issues", d["issues"], "#A5B4FC"),
        ("Private contributions", d["private"], "#5EEAD4"),
        ("Stars earned", d["stars"], AMBER),
        ("Followers", d["followers"], CYAN),
        ("Public repositories", d["repos"], TEXT),
    ]
    x0, y0, lh = 224, 84, 28
    p.append(f'<g font-family="{MONO}" font-size="12">')
    for i, (label, val, color) in enumerate(rows):
        y = y0 + i * lh
        b = round(0.2 + i * 0.14, 2)
        p.append(f'  <g opacity="1"><animate attributeName="opacity" values="0;0;1;1" '
                 f'keyTimes="0;{b/8:.4f};{(b+0.5)/8:.4f};1" dur="8s" repeatCount="indefinite"/>'
                 f'<circle cx="{x0}" cy="{y-4}" r="3" fill="{color}"/>'
                 f'<text x="{x0+14}" y="{y}" fill="{TEXT}">{esc(label)}</text>'
                 f'<text x="{W-24}" y="{y}" fill="{color}" text-anchor="end" font-weight="600">{val}</text></g>')
    p.append("</g>")
    p.append(f'<rect x="24" y="{H-18}" width="{W-48}" height="3" rx="1.5" fill="url(#accent)" opacity="0.7"/>')
    p.append("</svg>")
    open(path, "w").write("\n".join(p) + "\n")


def card_langs(d, path):
    W, H = 500, 320
    p = [shell(W, H, "LANGUAGES", f'{d["lang_count"]} across public repos')]
    langs = d["langs"]

    # stacked bar
    x = 24.0
    bw = W - 48
    p.append('<g>')
    for i, (name, frac, color) in enumerate(langs):
        seg = max(bw * frac, 2)
        p.append(f'  <rect x="{x:.1f}" y="62" width="{seg:.1f}" height="12" fill="{color}">'
                 f'<animate attributeName="opacity" values="0.55;1;0.55" dur="4s" begin="{i*0.25:.2f}s" '
                 f'repeatCount="indefinite"/></rect>')
        x += seg
    p.append('</g>')

    y0, lh = 108, 26
    barx, barw = 190, 210
    p.append(f'<g font-family="{MONO}" font-size="12">')
    for i, (name, frac, color) in enumerate(langs):
        y = y0 + i * lh
        w = max(barw * frac, 3)
        b = round(0.25 + i * 0.16, 2)
        k1, k2 = b / 8, (b + 1.0) / 8
        p.append(f'  <circle cx="{30}" cy="{y-4}" r="4" fill="{color}"/>')
        p.append(f'  <text x="44" y="{y}" fill="{TEXT}">{esc(name)}</text>')
        p.append(f'  <rect x="{barx}" y="{y-11}" width="{barw}" height="12" rx="6" fill="#0B1220" stroke="#123847"/>')
        p.append(f'  <rect x="{barx}" y="{y-11}" width="{w:.1f}" height="12" rx="6" fill="{color}" opacity="0.9">'
                 f'<animate attributeName="width" values="0;0;{w:.1f};{w:.1f}" keyTimes="0;{k1:.4f};{k2:.4f};1" '
                 f'dur="8s" repeatCount="indefinite"/></rect>')
        p.append(f'  <clipPath id="lc{i}"><rect x="{barx}" y="{y-11}" width="{w:.1f}" height="12" rx="6"/></clipPath>')
        p.append(f'  <g clip-path="url(#lc{i})"><rect y="{y-11}" width="50" height="12" fill="url(#shine)">'
                 f'<animate attributeName="x" values="{barx-60};{barx+w:.1f}" dur="8s" begin="{b+1.0:.2f}s" '
                 f'repeatCount="indefinite"/></rect></g>')
        p.append(f'  <text x="{W-24}" y="{y}" fill="{DIM}" text-anchor="end" font-size="11">{frac*100:.1f}%</text>')
    p.append("</g>")
    p.append(f'<rect x="24" y="{H-18}" width="{W-48}" height="3" rx="1.5" fill="url(#accent)" opacity="0.7"/>')
    p.append("</svg>")
    open(path, "w").write("\n".join(p) + "\n")


def card_activity(d, path):
    weeks = d["weeks"][-53:]
    cell, gap = 13, 3
    grid_w = len(weeks) * (cell + gap)
    W = grid_w + 96
    H = 7 * (cell + gap) + 116
    p = [shell(W, H, "CONTRIBUTION ACTIVITY", "last 53 weeks")]

    ox, oy = 48, 78
    labels = ["", "Mon", "", "Wed", "", "Fri", ""]
    p.append(f'<g font-family="{MONO}" font-size="9" fill="{DIM}">')
    for i, lb in enumerate(labels):
        if lb:
            p.append(f'  <text x="{ox-8}" y="{oy + i*(cell+gap) + 10}" text-anchor="end">{lb}</text>')
    p.append("</g>")

    maxc = max((day["contributionCount"] for w in weeks for day in w["contributionDays"]), default=1) or 1
    p.append("<g>")
    for wi, w in enumerate(weeks):
        for di, day in enumerate(w["contributionDays"]):
            n = day["contributionCount"]
            if n == 0:
                lvl = 0
            else:
                ratio = n / maxc
                lvl = 1 if ratio <= 0.25 else 2 if ratio <= 0.5 else 3 if ratio <= 0.75 else 4
            x = ox + wi * (cell + gap)
            y = oy + di * (cell + gap)
            begin = round(wi * 0.055 + di * 0.02, 3)
            p.append(f'  <rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{HEAT[lvl]}">'
                     f'<animate attributeName="opacity" values="0.15;1;1" keyTimes="0;0.12;1" dur="9s" '
                     f'begin="{begin}s" repeatCount="indefinite"/></rect>')
    p.append("</g>")

    # sweeping highlight column
    p.append(f'<rect y="{oy-4}" width="{cell+4}" height="{7*(cell+gap)}" rx="4" fill="{CYAN}" opacity="0.14">'
             f'<animate attributeName="x" values="{ox-20};{ox+grid_w}" dur="9s" repeatCount="indefinite"/></rect>')

    ly = H - 26
    p.append(f'<g font-family="{MONO}" font-size="10" fill="{DIM}">'
             f'<text x="{ox}" y="{ly+4}">Less</text>')
    for i, c in enumerate(HEAT):
        p.append(f'  <rect x="{ox + 38 + i*16}" y="{ly-8}" width="12" height="12" rx="3" fill="{c}"/>')
    p.append(f'  <text x="{ox + 38 + len(HEAT)*16 + 6}" y="{ly+4}">More</text>')
    p.append(f'  <text x="{W-24}" y="{ly+4}" text-anchor="end" fill="{DIM}">'
             f'longest streak {d["longest_streak"]} days &#183; best day {d["best_day"]}</text></g>')
    p.append("</svg>")
    open(path, "w").write("\n".join(p) + "\n")


def card_highlights(d, path):
    items = [
        ("CURRENT STREAK", f'{d["current_streak"]}', "days", AMBER),
        ("LONGEST STREAK", f'{d["longest_streak"]}', "days", CYAN),
        ("BUSIEST DAY", f'{d["best_day"]}', "contributions", GREEN),
        ("STARS EARNED", f'{d["stars"]}', "across repos", AMBER),
        ("REPOSITORIES", f'{d["repos"]}', "public", "#5EEAD4"),
        ("FOLLOWERS", f'{d["followers"]}', "on GitHub", "#A5B4FC"),
    ]
    W, H = 1010, 150
    p = [shell(W, H, "HIGHLIGHTS", "generated from the GitHub API")]
    cw, gap = 156, 12
    x0 = 24
    for i, (label, val, unit, color) in enumerate(items):
        x = x0 + i * (cw + gap)
        b = round(0.2 + i * 0.18, 2)
        p.append(f'<g><animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{b/9:.4f};{(b+0.6)/9:.4f};1" '
                 f'dur="9s" repeatCount="indefinite"/>'
                 f'<rect x="{x}" y="62" width="{cw}" height="66" rx="10" fill="#0B1220" stroke="{color}" '
                 f'stroke-opacity="0.55"/>'
                 f'<rect x="{x}" y="62" width="{cw}" height="66" rx="10" fill="none" stroke="{color}">'
                 f'<animate attributeName="opacity" values="0.5;0;0.5" dur="3s" begin="{b}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-width" values="1;4;1" dur="3s" begin="{b}s" repeatCount="indefinite"/>'
                 f'</rect>'
                 f'<text x="{x+cw/2:.0f}" y="82" text-anchor="middle" fill="{DIM}" font-size="9" letter-spacing="2" '
                 f'font-family="{MONO}">{label}</text>'
                 f'<text x="{x+cw/2:.0f}" y="110" text-anchor="middle" fill="{color}" font-size="26" font-weight="700" '
                 f'font-family="{MONO}">{val}</text>'
                 f'<text x="{x+cw/2:.0f}" y="124" text-anchor="middle" fill="{DIM}" font-size="9" '
                 f'font-family="{MONO}">{unit}</text></g>')
    p.append("</svg>")
    open(path, "w").write("\n".join(p) + "\n")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    login = args[0] if args else os.environ.get("GH_LOGIN", "jugnu790")
    out = os.environ.get("OUT_DIR", "assets")
    os.makedirs(out, exist_ok=True)

    if "--mock" in sys.argv:
        globals()["MOCK"] = True
        user = mock_user()
    else:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("Set GH_TOKEN (or run with --mock).")
        user = fetch(login, token)

    d = digest(user)
    card_stats(d, f"{out}/stats.svg")
    card_langs(d, f"{out}/langs.svg")
    card_activity(d, f"{out}/activity.svg")
    card_highlights(d, f"{out}/highlights.svg")
    print(f"built 4 cards for {d['login']} at {datetime.now():%Y-%m-%d %H:%M} UTC")


if __name__ == "__main__":
    main()