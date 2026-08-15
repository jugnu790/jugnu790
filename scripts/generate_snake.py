import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

USERNAME = os.getenv(
    "GITHUB_USERNAME",
    "jugnu790"
)

OUTPUT_DIR = ROOT / "assets"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def main():
    print(
        "Contribution snake generation is handled by "
        "the GitHub Actions workflow."
    )

    print()
    print(
        f"GitHub username: {USERNAME}"
    )

    print()
    print(
        "Run:"
    )

    print(
        "  GitHub Actions → Generate Contribution Snake → Run workflow"
    )


if __name__ == "__main__":
    main()