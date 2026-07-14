#!/usr/bin/env python3
"""Keep the duplicated nav and footer blocks in every page honest.

WHY THIS EXISTS
---------------
asmaa.dev is a plain static site served straight off GitHub Pages from the repo
root. There is no build step, no bundler, no templating engine and no server-side
includes -- the browser gets the exact bytes that are committed. That means the
site header/nav and the footer have to be physically duplicated into every HTML
page. The duplication is deliberate; the drift is not.

Each page marks its copies with sentinel comments:

    <!-- @partial:nav start ... -->    ... <!-- @partial:nav end -->
    <!-- @partial:footer start ... --> ... <!-- @partial:footer end -->

The canonical text lives in includes/partials/nav.html and
includes/partials/footer.html (each file already contains its own sentinels).
This script re-stamps the region between the sentinels in every target page from
those canonical files, so a nav change is a one-file change plus one command.

USAGE
-----
    python3 tools/sync_partials.py            # rewrite pages in place
    python3 tools/sync_partials.py --check    # exit 1 if any page has drifted

Stdlib only. Run it from anywhere; paths resolve relative to the repo root.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PARTIALS_DIR = REPO_ROOT / "includes" / "partials"

# name -> canonical source file
PARTIALS = {
    "nav": PARTIALS_DIR / "nav.html",
    "footer": PARTIALS_DIR / "footer.html",
}

# Pages that deliberately have no nav/footer. projects.html is a redirect stub
# kept only so old inbound links don't 404.
EXCLUDED = {"projects.html"}

# Directories that are not part of the site and must never be stamped.
SKIP_DIRS = {"node_modules", "vendor", "includes", "tools", ".git", "public"}


def target_pages() -> list[Path]:
    """Every top-level *.html plus every <route>/index.html that shares the chrome.

    Globbing rather than an explicit list, so a new route (privacy/, terms/,
    disclaimer/, ...) is picked up automatically instead of silently drifting.
    """
    pages = [p for p in REPO_ROOT.glob("*.html") if p.name not in EXCLUDED]
    pages += [
        p
        for p in REPO_ROOT.glob("*/index.html")
        if not SKIP_DIRS.intersection(p.parts)
    ]
    return sorted(pages)


def load_partial(name: str) -> str:
    """Read a canonical partial (sentinels included) with trailing space trimmed."""
    path = PARTIALS[name]
    if not path.is_file():
        raise SystemExit(f"error: missing canonical partial: {path}")
    return path.read_text(encoding="utf-8").rstrip("\n")


def region_pattern(name: str) -> re.Pattern[str]:
    """Match a sentinel-delimited region, sentinels included."""
    return re.compile(
        r"<!--\s*@partial:%s start.*?@partial:%s end\s*-->" % (name, name),
        re.DOTALL,
    )


def stamp(html: str, name: str, canonical: str) -> tuple[str, bool]:
    """Replace the named region in `html`. Returns (new_html, changed)."""
    pattern = region_pattern(name)
    if not pattern.search(html):
        return html, False
    new_html = pattern.sub(lambda _m: canonical, html, count=1)
    return new_html, new_html != html


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="do not write; exit 1 if any page has drifted from the canonical partial",
    )
    args = parser.parse_args(argv)

    canonical = {name: load_partial(name) for name in PARTIALS}

    drifted: list[str] = []
    missing: list[str] = []
    written: list[str] = []

    for page in target_pages():
        original = page.read_text(encoding="utf-8")
        html = original
        found_any = False

        for name, text in canonical.items():
            if not region_pattern(name).search(html):
                missing.append(f"{page.relative_to(REPO_ROOT)}: no @partial:{name} region")
                continue
            found_any = True
            html, _ = stamp(html, name, text)

        if not found_any:
            continue

        if html == original:
            continue

        rel = str(page.relative_to(REPO_ROOT))
        if args.check:
            drifted.append(rel)
        else:
            page.write_text(html, encoding="utf-8")
            written.append(rel)

    for note in missing:
        print(f"warning: {note}", file=sys.stderr)

    if args.check:
        if drifted:
            print("Partials have drifted from includes/partials/:")
            for rel in drifted:
                print(f"  - {rel}")
            return 1
        print("Partials are in sync.")
        return 0

    if written:
        print("Re-stamped:")
        for rel in written:
            print(f"  - {rel}")
    else:
        print("Nothing to do; all pages already match includes/partials/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
