#!/usr/bin/env python3
"""Sync expert judge scores from published Google Sheet tabs.

Each judge fills their own tab (see scripts/judging-sheet-<judge>.csv). Every
tab is published to the web as CSV, and the URLs are provided via
JUDGE_SHEET_CSV_URLS (comma-separated; JUDGE_SHEET_CSV_URL still works for a
single tab). This script merges the rows into data/theme-scores.json, which the
site bakes in as the expert half of the leaderboard.

Each criterion is rated on a 1-3 scale (1 = weak, 2 = solid, 3 = outstanding).
Levels are rescaled to 0-100 so they line up with the community score.

Rows match themes by the `theme_id` column (the themes.json id, e.g. 2002) when
present, and fall back to the `theme` name otherwise.
"""

import csv
import io
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
THEMES_PATH = BASE_DIR / "data" / "themes.json"
OUTPUT_PATH = BASE_DIR / "data" / "theme-scores.json"

RUBRIC = [
    ("cultural_authenticity", 0.50),
    ("visual_craft", 0.50),
]

SCALE = {
    "1": "Weak",
    "2": "Solid",
    "3": "Outstanding",
}

LEVEL_WORDS = {
    "1": 1.0,
    "2": 2.0,
    "3": 3.0,
    "weak": 1.0,
    "solid": 2.0,
    "outstanding": 3.0,
}

COLUMN_ALIASES = {
    "cultural_authenticity": {"culturalauthenticity", "authenticity", "culture", "cultural", "heritage"},
    "visual_craft": {"visualcraft", "craft", "visuals", "visual", "aesthetics", "design"},
}

JUDGE_KEYS = {"judge", "judgename", "judgeid", "name", "judge_name"}
THEME_KEYS = {"theme", "themename", "entry", "theme_name"}
THEME_ID_KEYS = {"themeid", "themeidnumber", "themekey", "id"}

SCALE_MAX = 3.0


def normalize(value):
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_csv(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8-sig")


def sheet_urls():
    raw = (
        os.environ.get("JUDGE_SHEET_CSV_URLS")
        or os.environ.get("JUDGE_SHEET_CSV_URL")
        or ""
    )
    return [part.strip() for part in re.split(r"[,\n]", raw) if part.strip()]


def resolve_columns(fieldnames):
    mapping = {}
    for header in fieldnames or []:
        key = normalize(header)
        if key in JUDGE_KEYS:
            mapping["judge"] = header
        elif key in THEME_ID_KEYS:
            mapping["theme_id"] = header
        elif key in THEME_KEYS:
            mapping["theme"] = header
        else:
            for rubric_key, aliases in COLUMN_ALIASES.items():
                if key in aliases and rubric_key not in mapping:
                    mapping[rubric_key] = header
    return mapping


def parse_level(raw):
    text = (raw or "").strip().lower().replace(",", ".")
    if not text:
        return None
    if text in LEVEL_WORDS:
        return LEVEL_WORDS[text]
    try:
        value = float(text)
    except ValueError:
        return None
    if value < 1 or value > SCALE_MAX:
        return None
    return value


def build_theme_lookup(themes):
    lookup = {}
    for theme in themes:
        for token in (theme.get("name"), theme.get("id")):
            if token:
                lookup[normalize(token)] = theme["id"]
    return lookup


def match_theme(lookup, raw):
    key = normalize(raw)
    if key in lookup:
        return lookup[key]
    for token, theme_id in lookup.items():
        if token and (token in key or key in token):
            return theme_id
    return None


def ingest(raw, lookup, valid_ids, totals, judges):
    reader = csv.DictReader(io.StringIO(raw))
    columns = resolve_columns(reader.fieldnames)

    missing = [key for key, _ in RUBRIC if key not in columns]
    if "judge" not in columns or not ("theme_id" in columns or "theme" in columns) or missing:
        raise ValueError(f"missing expected columns (found {reader.fieldnames})")

    for row in reader:
        judge = (row.get(columns["judge"]) or "").strip()
        raw_id = (row.get(columns.get("theme_id", "")) or "").strip()
        raw_name = (row.get(columns.get("theme", "")) or "").strip()
        if not judge or not (raw_id or raw_name):
            continue

        theme_id = None
        if raw_id:
            theme_id = raw_id if raw_id in valid_ids else match_theme(lookup, raw_id)
        if not theme_id and raw_name:
            theme_id = match_theme(lookup, raw_name)
        if not theme_id:
            print(f"warn: unmatched theme '{raw_id or raw_name}' (judge {judge})", file=sys.stderr)
            continue

        if judge not in judges:
            judges.append(judge)

        levels = {key: parse_level(row.get(columns[key])) for key, _ in RUBRIC}
        if any(value is None for value in levels.values()):
            continue

        total = sum((levels[key] / SCALE_MAX) * weight for key, weight in RUBRIC) * 100
        totals.setdefault(theme_id, []).append(round(total, 1))


def main():
    urls = sheet_urls()
    if not urls:
        print("JUDGE_SHEET_CSV_URLS not set; skipping judge score sync.")
        return 0

    themes = json.loads(THEMES_PATH.read_text(encoding="utf-8"))
    lookup = build_theme_lookup(themes)
    valid_ids = {theme["id"] for theme in themes}

    totals = {}
    judges = []
    for url in urls:
        try:
            raw = fetch_csv(url)
        except Exception as exc:
            print(f"error: could not fetch judge sheet {url}: {exc}", file=sys.stderr)
            return 1
        try:
            ingest(raw, lookup, valid_ids, totals, judges)
        except ValueError as exc:
            print(f"error: {url}: {exc}", file=sys.stderr)
            return 1

    scores_out = {}
    for theme in themes:
        entries = totals.get(theme["id"], [])
        if entries:
            scores_out[theme["id"]] = {
                "average": round(sum(entries) / len(entries), 1),
                "count": len(entries),
            }

    existing = None
    if OUTPUT_PATH.exists():
        try:
            existing = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = None

    if (
        existing
        and existing.get("scores") == scores_out
        and existing.get("judges") == judges
    ):
        print(f"No judge score changes: {scores_out}")
        return 0

    payload = {
        "updatedAt": now_iso(),
        "scale": SCALE,
        "rubric": {key: weight for key, weight in RUBRIC},
        "judges": judges,
        "scores": scores_out,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Updated {OUTPUT_PATH.relative_to(BASE_DIR)} -> {scores_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
