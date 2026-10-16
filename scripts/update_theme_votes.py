#!/usr/bin/env python3
"""Refresh the theme competition vote counts from GitHub reactions.

Runs in CI with an authenticated `gh` (GITHUB_TOKEN), so it never touches the
60/hr unauthenticated limit that browsers share. Writes data/theme-votes.json
only when the counts actually change, so it does not spam commits.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
THEMES_PATH = BASE_DIR / "data" / "themes.json"
OUTPUT_PATH = BASE_DIR / "data" / "theme-votes.json"

POSITIVE_REACTIONS = ("+1", "heart", "hooray", "rocket", "laugh")
REPO = os.environ.get("GITHUB_REPOSITORY", "nebiyuelias1/omarchy-ethiopia")


def reaction_total(reactions):
    return sum(int(reactions.get(name, 0)) for name in POSITIVE_REACTIONS)


def fetch_issue_reactions(number):
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/issues/{number}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"warn: could not read issue #{number}: {result.stderr.strip()}", file=sys.stderr)
        return None
    data = json.loads(result.stdout)
    return reaction_total(data.get("reactions") or {})


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main():
    if not THEMES_PATH.exists():
        print(f"error: {THEMES_PATH} not found", file=sys.stderr)
        return 1

    themes = json.loads(THEMES_PATH.read_text(encoding="utf-8"))

    votes = {}
    for theme in themes:
        number = theme.get("issue")
        if not isinstance(number, int):
            continue
        total = fetch_issue_reactions(number)
        votes[theme["id"]] = 0 if total is None else total

    existing = None
    if OUTPUT_PATH.exists():
        try:
            existing = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = None

    if existing and existing.get("votes") == votes:
        print(f"No vote changes: {votes}")
        return 0

    payload = {"updatedAt": now_iso(), "votes": votes}
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Updated {OUTPUT_PATH.relative_to(BASE_DIR)} -> {votes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
