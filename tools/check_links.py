#!/usr/bin/env python3
"""Validate every link on the site: local files on disk, and external URLs over the network.

WHY THIS EXISTS
---------------
The site is served raw by GitHub Pages, so a bad href is a 404 in production with
nothing to catch it. This checks both halves:

  * LOCAL   -- every root-absolute href/src resolves to a real file, matched
               CASE-SENSITIVELY. macOS is case-insensitive and GitHub Pages is not,
               so `/assets/Foo.PNG` can work locally and 404 in production.
  * EXTERNAL-- every http(s) URL is reachable. Some hosts (LinkedIn, for one) reject
               HEAD with 405 while serving GET fine, so a HEAD failure is retried
               with GET before it is called broken.

Route mapping mirrors what GitHub Pages actually does:
    "/"                 -> index.html
    "/privacy/"         -> privacy/index.html
    "/case-studies.html"-> case-studies.html

Canonical/og URLs pointing at https://asmaa.dev/... are expected to 404 until the
branch is deployed. They are reported separately as PENDING DEPLOY -- and only if
the corresponding LOCAL route resolves. If the local route is missing too, that is a
real error, not a deploy artifact.

USAGE
-----
    python3 tools/check_links.py            # local + external
    python3 tools/check_links.py --local    # skip the network
Exit code is 1 if anything is genuinely broken.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_ORIGIN = "https://asmaa.dev"
UA = {"User-Agent": "Mozilla/5.0 (compatible; asmaa.dev link-check)"}
TIMEOUT = 15

LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')
SRCSET_RE = re.compile(r'srcset="([^"]+)"')


def pages() -> list[Path]:
    found = sorted(REPO_ROOT.glob("*.html"))
    found += sorted(REPO_ROOT.glob("*/index.html"))
    return [p for p in found if "node_modules" not in p.parts and "vendor" not in p.parts]


def resolve_local(ref: str) -> Path:
    """Map a root-absolute URL path to the file GitHub Pages would serve."""
    path = ref.split("#")[0].split("?")[0]
    if path.endswith("/"):
        path += "index.html"          # "/" -> index.html, "/privacy/" -> privacy/index.html
    return REPO_ROOT / path.lstrip("/")


def exists_case_sensitive(p: Path) -> bool:
    """Path.exists() is case-insensitive on macOS; compare against the real dirent."""
    try:
        return p.name in {e.name for e in p.parent.iterdir()}
    except (FileNotFoundError, NotADirectoryError):
        return False


# Anti-bot responses. The URL is not broken -- the host simply refuses to be checked
# by a script. LinkedIn serves 999 to non-browser clients and bounces logged-out
# visitors to an authwall; a human with a session reaches the page fine. Calling these
# "broken" would be a false alarm, so they are reported as UNVERIFIABLE, not failures.
BOT_BLOCKED = {999, 429}


def fetch(url: str) -> tuple[str, str]:
    """Return (status, note) where status is 'ok', 'blocked', or 'broken'.

    HEAD first, falling back to GET for hosts that reject HEAD (405/403/...).
    """
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=UA)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return "ok", f"{r.status} ({method})"
        except urllib.error.HTTPError as e:
            if e.code in BOT_BLOCKED:
                return "blocked", f"HTTP {e.code} (anti-bot)"
            if method == "HEAD" and e.code in (403, 405, 400, 501):
                continue          # host dislikes HEAD -- retry with GET
            return "broken", f"HTTP {e.code}"
        except Exception as e:                      # noqa: BLE001
            if method == "HEAD":
                continue
            return "broken", f"{type(e).__name__}: {e}"
    return "broken", "unreachable"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--local", action="store_true", help="skip external URL checks")
    args = ap.parse_args()

    local_refs: dict[str, set[str]] = {}
    external: dict[str, set[str]] = {}

    for page in pages():
        text = page.read_text(encoding="utf-8")
        rel = str(page.relative_to(REPO_ROOT))
        refs = LINK_RE.findall(text)
        for s in SRCSET_RE.findall(text):
            refs += [c.strip().split()[0] for c in s.split(",") if c.strip()]

        for ref in refs:
            if ref.startswith(("mailto:", "tel:", "data:", "#", "javascript:")):
                continue
            if ref.startswith("http"):
                external.setdefault(ref, set()).add(rel)
            elif ref.startswith("/"):
                local_refs.setdefault(ref, set()).add(rel)

    broken: list[str] = []
    pending: list[str] = []

    print(f"LOCAL  ({len(local_refs)} unique refs)")
    for ref in sorted(local_refs):
        target = resolve_local(ref)
        if exists_case_sensitive(target):
            continue
        broken.append(f"{ref}  (from {', '.join(sorted(local_refs[ref]))})")
    print("  broken: " + (f"{len(broken)}" if broken else "none"))
    for b in broken:
        print(f"    MISSING {b}")

    blocked: list[str] = []

    if not args.local:
        print(f"\nEXTERNAL  ({len(external)} unique URLs)")
        for url in sorted(external):
            status, note = fetch(url)
            if status == "ok":
                print(f"  ok      {note:<18} {url}")
                continue
            if status == "blocked":
                blocked.append(f"{url}  ({note})")
                print(f"  blocked {note:<18} {url}")
                continue
            # A not-yet-deployed canonical/og URL is fine *iff* its local route resolves.
            if url.startswith(SITE_ORIGIN):
                route = url[len(SITE_ORIGIN):] or "/"
                if exists_case_sensitive(resolve_local(route)):
                    pending.append(url)
                    print(f"  pending {'not deployed yet':<18} {url}  (local route resolves)")
                    continue
            broken.append(f"{url}  ({note})")
            print(f"  BROKEN  {note:<18} {url}")

    print("\n" + "=" * 60)
    if pending:
        print(f"{len(pending)} URL(s) pending deploy (expected until the branch ships):")
        for p in pending:
            print(f"  - {p}")
    if blocked:
        print(f"{len(blocked)} URL(s) unverifiable — host blocks automated checks (not broken):")
        for b in blocked:
            print(f"  - {b}")
    if broken:
        print(f"BROKEN: {len(broken)}")
        for b in broken:
            print(f"  - {b}")
        return 1
    print("All links resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
