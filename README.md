# 👋 Hi, I'm Deepesh Upadhyay

<p align="center">
  <img src="./assets/hero.svg" alt="Deepesh Upadhyay" width="100%">
</p>

<p align="center">
  <a href="https://github.com/jugnu790">
    <img src="https://img.shields.io/badge/GitHub-jugnu790-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
</p>

## 🚀 About Me

I'm a software developer interested in building scalable applications, data engineering solutions, automation, distributed systems, and modern software technologies.

I enjoy working on practical engineering problems and turning complex workflows into maintainable, automated systems.

---

## ⚡ GitHub Activity

<p align="center">
  <img src="./assets/activity.svg" alt="GitHub activity" width="100%">
</p>

---

<!-- AUTO-GENERATED-START -->

## 📊 Live GitHub Statistics

<p align="center">

<img
src="./assets/stats-card.svg"
alt="GitHub statistics"
/>

</p>

| Metric | Value |
|---|---:|
| Repositories | 27 |
| Stars | 24 |
| Forks | 0 |
| Followers | 2 |
| Following | 3 |

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

`2026-08-15 21:50 UTC`

<!-- AUTO-GENERATED-END -->



---

## 🛠️ Technologies
>>>>>>> 15709f53141cb39e3ae777011ba3c6d959b7ff69

<p align="center">
  <img src="./assets/stats-card.svg" alt="GitHub statistics">
</p>

| Metric | Value |
|:---|---:|
| Repositories | Automatically updated |
| Stars | Automatically updated |
| Forks | Automatically updated |
| Followers | Automatically updated |
| Following | Automatically updated |

---

## 🐍 Contribution Snake

<p align="center">
  <img
    src="./assets/github-contribution-grid-snake.svg"
    alt="GitHub contribution snake"
  >
</p>

---

## 💻 Languages

<p align="center">
  <img
    src="./assets/languages-card.svg"
    alt="Programming languages"
  >
</p>

---

## 🚀 Top Repositories

<p align="center">
  <img
    src="./assets/repositories-card.svg"
    alt="Top repositories"
  >
</p>

---

### 🔄 Automated Updates

This section is generated automatically from GitHub data using GitHub Actions and Python.

<!-- AUTO-GENERATED-END -->

---

## 🛠️ Technologies & Skills

<p align="center">
  <img src="./assets/skills.svg" alt="Skills" width="100%">
</p>

---

## 🏗️ Data & Automation Architecture

<p align="center">
  <img src="./assets/architecture.svg" alt="Architecture" width="100%">
</p>

The profile automation pipeline follows this flow:

```text
GitHub API
    │
    ▼
fetch_data.py
    │
    ▼
process_data.py
    │
    ▼
build_cards.py
    │
    ├── stats-card.svg
    ├── languages-card.svg
    └── repositories-card.svg
    │
    ▼
update_readme.py
    │
    ▼
README.md
    │
    ▼
GitHub Profile
```

---

## 🔄 Automation

This repository uses GitHub Actions to automate profile data and visualizations.

### Automated tasks

- Fetch GitHub profile data
- Fetch repository information
- Process repository statistics
- Calculate programming-language statistics
- Generate SVG statistics cards
- Generate the contribution snake
- Update the README automatically
- Commit generated changes back to the repository
- Run scheduled updates

### Update frequency

The workflows are scheduled to run automatically. They can also be started manually from the **Actions** tab.

> GitHub Actions provides scheduled automation, not second-by-second real-time updates. The actual refresh interval depends on the workflow schedule.

---

## 📈 GitHub Data Pipeline

```text
┌──────────────────┐
│    GitHub API    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  fetch_data.py   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ process_data.py  │
└────────┬─────────┘
         │
         ├───────────────┐
         ▼               ▼
┌────────────────┐  ┌──────────────────┐
│ build_cards.py │  │ generate_snake   │
└───────┬────────┘  └────────┬─────────┘
        │                    │
        ▼                    ▼
   SVG statistics       Snake animation
        │                    │
        └─────────┬──────────┘
                  ▼
        ┌──────────────────┐
        │ update_readme.py │
        └────────┬─────────┘
                 │
                 ▼
            README.md
```

---

## 📁 Project Structure

```text
jugnu790/
│
├── .github/
│   └── workflows/
│       ├── deploy.yml
│       ├── generate-snake.yml
│       ├── update-data.yml
│       └── update-stats.yml
│
├── assets/
│   ├── activity.svg
│   ├── architecture.svg
│   ├── divider.svg
│   ├── footer.svg
│   ├── hero.svg
│   ├── highlights.svg
│   ├── kafka.svg
│   ├── langs.svg
│   ├── loop.svg
│   ├── orbit.svg
│   ├── pipeline.svg
│   ├── skills.svg
│   ├── stats.svg
│   └── terminal.svg
│
├── scripts/
│   ├── build_cards.py
│   ├── fetch_data.py
│   ├── generate_snake.py
│   ├── process_data.py
│   └── update_readme.py
│
├── README.md
└── requirements.txt
```

---

## 🔧 Technologies Used

<p align="center">
  <img src="./assets/langs.svg" alt="Languages and technologies" width="100%">
</p>

- Python
- GitHub REST API
- GitHub Actions
- YAML
- SVG
- Git
- GitHub Pages
- Automation pipelines

---

## 🧩 How the Automation Works

1. GitHub Actions starts the scheduled workflow.
2. `fetch_data.py` retrieves current GitHub data.
3. The raw data is stored in the `data/` directory.
4. `process_data.py` converts the raw data into useful statistics.
5. `build_cards.py` generates SVG cards.
6. The snake workflow generates the contribution animation.
7. `update_readme.py` updates the automatically generated section.
8. GitHub Actions commits the changed generated files.
9. The updated README and assets are displayed on GitHub.

---

## 🧪 Manual Update

To force an update immediately:

```text
GitHub Repository
      ↓
Actions
      ↓
Select workflow
      ↓
Run workflow
```

This is useful when you don't want to wait for the next scheduled run.

---

## 🔐 GitHub Actions Permissions

The automation requires repository workflow permissions that allow GitHub Actions to write generated files back to the repository.

Recommended setting:

```text
Repository
  → Settings
  → Actions
  → General
  → Workflow permissions
  → Read and write permissions
```

Do not put a personal GitHub password or personal access token directly into the repository.

The built-in `GITHUB_TOKEN` should be used where possible.

---

## 📌 Important

This project is designed for automated GitHub profile presentation and statistics.

The generated information comes from GitHub data and may change whenever GitHub updates the underlying account or repository information.

---

## 🔗 GitHub

<p align="center">
  <a href="https://github.com/jugnu790">
    <img
      src="https://img.shields.io/badge/Visit%20My%20GitHub-jugnu790-181717?style=for-the-badge&logo=github"
      alt="Visit GitHub"
    >
  </a>
</p>

---

<p align="center">
  <sub>Built and maintained with Python, GitHub Actions, and automation.</sub>
</p>
