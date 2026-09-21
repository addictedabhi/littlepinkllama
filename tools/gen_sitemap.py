# -*- coding: utf-8 -*-
"""Generator for sitemap.xml.

Reads the same scraped product/collection data as gen.py (argv[1] = scratch
dir) so the URL list never drifts from the actual generated pages. Safe to
re-run; writes sitemap.xml at the repo root.

Site base URL: the production custom domain (see CNAME at repo root).
Kept as gen.SITE_URL — the single source of truth also used for canonical
links, OG/Twitter tags and JSON-LD, so it never drifts out of sync here.
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = gen.SITE_URL
TODAY = datetime.date.today().isoformat()

STATIC_PAGES = [
    ("", "weekly", "1.0"),
    ("pages/about-us.html", "monthly", "0.7"),
    ("pages/contact.html", "monthly", "0.5"),
    ("pages/faq.html", "monthly", "0.5"),
    ("pages/shipping-policy.html", "yearly", "0.3"),
    ("pages/return-policy.html", "yearly", "0.3"),
    ("pages/terms-of-service.html", "yearly", "0.3"),
    ("pages/privacy-policy.html", "yearly", "0.3"),
    ("pages/sitemap.html", "monthly", "0.3"),
    ("blogs/index.html", "weekly", "0.6"),
]

COLLECTIONS = ["all", "brooches", "hairclips", "crochet-toys", "collar", "rakhis", "featured-products"]

BLOG_POSTS = [
    "hair-clip-care-tips-for-kids",
    "why-handmade-beats-mass-produced",
    "why-a-brooch-is-more-than-an-accessory-for-your-little-one",
]


def url_entry(loc, changefreq, priority):
    return (
        "  <url>\n"
        f"    <loc>{BASE_URL}/{loc}</loc>\n"
        f"    <lastmod>{TODAY}</lastmod>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>"
    )


def build():
    entries = []
    for loc, freq, pri in STATIC_PAGES:
        entries.append(url_entry(loc, freq, pri))
    for c in COLLECTIONS:
        entries.append(url_entry(f"collections/{c}.html", "weekly", "0.8"))
    for handle in gen.prods.keys():
        entries.append(url_entry(f"products/{handle}.html", "weekly", "0.8"))
    for slug in BLOG_POSTS:
        entries.append(url_entry(f"blogs/{slug}.html", "monthly", "0.6"))

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    out_path = os.path.join(SITE, "sitemap.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"wrote sitemap.xml — {len(entries)} URLs")


if __name__ == "__main__":
    build()
