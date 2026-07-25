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

from build_local_pages import CITIES, INDUSTRIES, SERVICES, SITE, footer_areas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LASTMOD = "2026-07-24"

# Existing pages, preserved with their original priorities.
EXISTING = [
    ("", "weekly", "1.0"),
    ("time-money-audit.html", "monthly", "0.9"),
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
    "time-money-audit.html",
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
        lines.append(f"    <lastmod>{LASTMOD}</lastmod>")
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
