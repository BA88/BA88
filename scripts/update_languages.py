#!/usr/bin/env python3
"""Draw a "most used languages" chart from GitHub's language stats.

Sums the bytes per language that GitHub reports for every repo the token's
owner has, private repos included. Writes assets/languages.svg (a stacked bar
and a two-column legend) and points README.md at it, between the markers
<!-- langs:start --> and <!-- langs:end -->.

Leaves out DEFAULT_EXCLUDE_REPOS and DEFAULT_EXCLUDE_LANGS; the flags add more.

Requires the gh CLI, logged in or given GH_TOKEN. Uses only the standard library.

Example:
    ./scripts/update_languages.py
    ./scripts/update_languages.py --exclude-lang Shell --dry-run
"""

import argparse
import json
import subprocess
import sys
from collections import Counter
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
SVG = ROOT / "assets" / "languages.svg"
START = "<!-- langs:start -->"
END = "<!-- langs:end -->"

DEFAULT_EXCLUDE_REPOS = {"tuck_dotfile"}
DEFAULT_EXCLUDE_LANGS = {"HTML", "CSS", "Typst"}

# Assigned by rank, largest language first.
# Text is one mid gray (#7d8590) so it reads on GitHub's light and dark themes;
# an SVG in an <img> sees the OS color scheme, not GitHub's theme setting.
PALETTE =["#4f7cac", "#c0843d", "#6a9f6a", "#a3628c", "#5aa0a8", "#b85c50"]

WIDTH = 460
BAR_Y = 52
BAR_HEIGHT = 10
ROW_START = 92
ROW_GAP = 28


def gh_json(args):
    result = subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout)


def owned_repos():
    repos = gh_json(
        ["repo", "list", "--limit", "1000", "--source", "--json", "nameWithOwner"]
    )
    return [r["nameWithOwner"] for r in repos]


def language_totals(repos, exclude_repos, exclude_langs):
    totals = Counter()
    for full_name in repos:
        if full_name.split("/", 1)[1] in exclude_repos:
            continue
        for lang, size in gh_json(["api", f"repos/{full_name}/languages"]).items():
            if lang not in exclude_langs:
                totals[lang] += size
    return totals


def shares(totals, top):
    """Return (language, percent) pairs for the top languages, summing to 100."""
    kept = totals.most_common(top)
    grand = sum(size for _, size in kept)
    return [(lang, 100 * size / grand) for lang, size in kept]


def render_svg(rows):
    rows_per_col = (len(rows) + 1) // 2
    height = ROW_START + (rows_per_col - 1) * ROW_GAP + 20
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
        f'height="{height}" viewBox="0 0 {WIDTH} {height}">',
        "<style>",
        "text { font: 14px -apple-system, 'Segoe UI', Helvetica, Arial,"
        " sans-serif; fill: #7d8590; }",
        ".title { font-size: 18px; font-weight: 600; }",
        "</style>",
        '<text class="title" x="0" y="24">Most used languages</text>',
        f'<clipPath id="bar"><rect x="0" y="{BAR_Y}" width="{WIDTH}" '
        f'height="{BAR_HEIGHT}" rx="{BAR_HEIGHT // 2}"/></clipPath>',
        '<g clip-path="url(#bar)">',
    ]
    x = 0.0
    for i, (_, pct) in enumerate(rows):
        w = WIDTH * pct / 100
        parts.append(
            f'<rect x="{x:.2f}" y="{BAR_Y}" width="{w:.2f}" '
            f'height="{BAR_HEIGHT}" fill="{PALETTE[i % len(PALETTE)]}"/>'
        )
        x += w
    parts.append("</g>")
    for i, (lang, pct) in enumerate(rows):
        col, row = divmod(i, rows_per_col)
        cx = col * WIDTH / 2 + 6
        cy = ROW_START + row * ROW_GAP
        parts.append(
            f'<circle cx="{cx:.0f}" cy="{cy - 5}" r="6" '
            f'fill="{PALETTE[i % len(PALETTE)]}"/>'
        )
        parts.append(
            f'<text x="{cx + 14:.0f}" y="{cy}">{escape(lang)} {pct:.1f}%</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def readme_block(rows):
    alt = "Most used languages: " + ", ".join(
        f"{lang} {pct:.1f}%" for lang, pct in rows
    )
    return f'<img src="assets/languages.svg" alt="{escape(alt)}">'


def replace_block(text, block):
    if START not in text or END not in text:
        sys.exit(f"README.md needs both {START} and {END} markers.")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{START}\n{block}\n{END}{tail}"


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--exclude-repo", action="append", default=[], metavar="NAME",
        help="another repo name to leave out; repeat for more",
    )
    parser.add_argument(
        "--exclude-lang", action="append", default=[], metavar="LANG",
        help="another language to leave out, as GitHub names it; repeat for more",
    )
    parser.add_argument(
        "--top", type=int, default=6, help="number of languages to show (default 6)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="print the percentages; write nothing",
    )
    args = parser.parse_args()

    totals = language_totals(
        owned_repos(),
        DEFAULT_EXCLUDE_REPOS | set(args.exclude_repo),
        DEFAULT_EXCLUDE_LANGS | set(args.exclude_lang),
    )
    if not totals:
        sys.exit("No language data found.")
    rows = shares(totals, args.top)

    if args.dry_run:
        for lang, pct in rows:
            print(f"{lang} {pct:.1f}%")
        return
    SVG.parent.mkdir(exist_ok=True)
    SVG.write_text(render_svg(rows))
    README.write_text(replace_block(README.read_text(), readme_block(rows)))
    print(f"Updated {SVG} and {README}")


if __name__ == "__main__":
    main()
