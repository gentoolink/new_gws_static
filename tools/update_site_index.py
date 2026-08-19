#!/usr/bin/env python3
"""
Keeps sitemap.xml and the footer service-area links in sync with the pages
produced by build_local_pages.py.

Run after build_local_pages.py:

    python tools/build_local_pages.py
    python tools/update_site_index.py
"""

import os
import re
import subprocess

from build_local_pages import CITIES, INDUSTRIES, SERVICES, SITE, footer_areas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Fallback only — used when git isn't available or a page has no history yet.
# Every other lastmod is derived per-page from git; see lastmod_for().
LASTMOD_FALLBACK = "2026-08-12"

# Footer/nav link churn touches every page at once and is not a content change.
# Stamping the whole site with today's date because a footer link moved is the
# thing that makes Google stop trusting lastmod, so those commits are skipped
# when working out when a page last actually changed.
MECHANICAL = re.compile(
    r'footer-areas|footer-services-label|footer-area-current|'
    r'ai-visibility-audit\.html" style="font-size:13px|'
    r'(google-business-profile-management|ai-phone-receptionist|'
    r'website-hosting-care-plans)\.html">|'
    r'web-design-(prince-george|vanderhoof|fort-st-james|fraser-lake|'
    r'burns-lake|quesnel)\.html">|'
    r'^</?(div|span)>$|^$'
)


def _git(*args):
    """Run a git command in the repo root, returning stdout ('' on failure)."""
    try:
        return subprocess.run(
            ("git",) + args, cwd=ROOT, capture_output=True,
            encoding="utf-8", errors="replace", check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def lastmod_for(path):
    """Date of the last commit that made a real content change to `path`.

    Walks back through history skipping commits whose only edits to this file
    were the sitewide footer/nav link blocks, so a link rollout doesn't reset
    every page's freshness date.
    """
    name = path or "index.html"
    log = _git("log", "--format=%H|%ad", "--date=short", "--", name).strip()
    for line in log.splitlines():
        sha, date = line.split("|")
        diff = _git("show", "--format=", "--unified=0", sha, "--", name)
        changed = [
            l[1:].strip() for l in diff.splitlines()
            if l[:1] in "+-" and not l.startswith(("+++", "---"))
        ]
        if not changed:
            continue
        if all(MECHANICAL.search(l) for l in changed):
            continue
        return date
    return LASTMOD_FALLBACK


# Existing pages, preserved with their original priorities.
EXISTING = [
    ("", "weekly", "1.0"),
    ("ai-visibility-audit.html", "monthly", "0.9"),
    ("services.html", "monthly", "0.9"),
    ("contact.html", "monthly", "0.8"),
    ("about.html", "monthly", "0.7"),
    ("blog.html", "weekly", "0.7"),
    ("templates.html", "monthly", "0.6"),
    ("blog-ai-saves-small-business-time.html", "yearly", "0.6"),
    ("blog-semantic-markup-ai-ready.html", "yearly", "0.6"),
    # media.html is parked (thin content) — gitignored and 302'd in .htaccess.
    ("privacy-policy.html", "yearly", "0.3"),
]

# Pages that should carry the footer service-area link hub.
FOOTER_HUB_PAGES = [
    "index.html",
    "services.html",
    "contact.html",
    "about.html",
    "blog.html",
    "templates.html",
]


def build_sitemap():
    entries = list(EXISTING)
    # City pages rank as primary commercial landing pages.
    for c in CITIES:
        entries.append((f'{c["slug"]}.html', "monthly", "0.8"))
    # Standalone service pages sit alongside services.html in importance.
    for s in SERVICES:
        entries.append((f'{s["slug"]}.html', "monthly", "0.8"))
    for i in INDUSTRIES:
        entries.append((f'{i["slug"]}.html', "monthly", "0.7"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, freq, pri in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{SITE}/{path}</loc>")
        lines.append(f"    <lastmod>{lastmod_for(path)}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{pri}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")

    out = "\n".join(lines) + "\n"
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print(f"sitemap.xml — {len(entries)} URLs")


def inject_footer_hub():
    """Adds the service-area link hub to existing pages that don't have one."""
    block_inner = footer_areas(current_slug=None)
    block = (
        '    <div class="footer-areas">\n'
        '      <span class="footer-areas-label">Serving Northern BC</span>\n'
        '      <span class="footer-areas-links">\n'
        f"{block_inner}\n"
        "      </span>\n"
        "    </div>\n"
    )

    for name in FOOTER_HUB_PAGES:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            print(f"  skip {name} (missing)")
            continue
        src = open(path, encoding="utf-8").read()
        if 'class="footer-areas"' in src:
            print(f"  skip {name} (already has hub)")
            continue
        m = re.search(r'^([ \t]*)<p class="footer-copy">', src, re.M)
        if not m:
            print(f"  skip {name} (no footer-copy anchor)")
            continue
        src = src[: m.start()] + block + src[m.start():]
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)
        print(f"  updated {name}")


if __name__ == "__main__":
    build_sitemap()
    print("Injecting footer service-area hub...")
    inject_footer_hub()
