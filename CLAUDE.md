# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Static replica of littlepinkllama.com (the owner's Shopify kids-accessories store) with **no payments, cart, or checkout by design**. Every order CTA is a WhatsApp deep link (`https://wa.me/919460074404`, prefilled with product name + price) or an Instagram DM link (`@little_pink_llama_`). The displayed contact phone number is +91 99998 25527 — different from the WhatsApp ordering number; don't "fix" one to match the other. Never introduce payment, cart, or checkout functionality.

Plain HTML/CSS/JS, zero dependencies, no build step. Deployed to GitHub Pages by `.github/workflows/deploy.yml` on push to `main`, served at the custom domain `littlepinkllama.com` (see `CNAME` at repo root — GitHub Pages requires this file to serve a custom domain instead of the `github.io` default).

## Commands

```
python -m http.server 8080        # run locally from repo root
python tools/gen.py <scratch-dir>        # regenerate home/collections/products
python tools/gen_pages.py <scratch-dir>  # regenerate about/contact/FAQ/policies/blogs/sitemap
python tools/gen_404.py <scratch-dir>    # regenerate 404.html
python tools/gen_sitemap.py <scratch-dir>  # regenerate sitemap.xml
```

There is no test suite. Verification = serve locally, check pages return 200, no broken links/images, no console errors. Playwright (Python) is available on this machine for screenshots.

## Architecture — generated site, two sources of truth

The ~74 HTML pages were **generated** by `tools/gen.py` and `tools/gen_pages.py` from data scraped off the live Shopify store (catalog via `/products.json`, page content via HTML). The generators need that scraped-data directory as `argv[1]` — it lives in a session scratchpad, so if it's gone, re-scrape the live store first or edit the committed HTML directly.

Consequence of this design: **for site-wide changes (header, footer, nav, product cards), edit the generator and regenerate — never hand-edit 74 files.** For one-off content tweaks, editing the HTML directly is fine, but know that a later regeneration will overwrite it; mirror any permanent change into the generator.

- `tools/gen.py` — shared `head()`/`header()`/`footer()`/`card()` used by every generator, plus homepage, 7 collection pages, 53 product pages. `gen_pages.py` and `gen_404.py` both import from it. `head()` also owns all SEO output (meta description, canonical link, OG/Twitter tags, JSON-LD `schema` param, `noindex` flag) — `SITE_URL` here (`https://littlepinkllama.com`) is the single source of truth for canonical/OG/sitemap URLs; `gen_sitemap.py` imports it rather than hardcoding its own.
- `tools/gen_pages.py` — content pages; sanitizes scraped Shopify markup (strips wrappers, rewrites internal links via `rewrite_internal_href()` — the one place that logic lives, shared by both the regex `sanitize()` pass and `ArticleRebuilder`, rewrites Razorpay/Shopify mentions to the WhatsApp ordering flow). `content_page(..., h1=...)` injects a real `<h1>` on pages whose scraped body has none (about-us, FAQ) and strips a redundant leading `<h2>` banner that would otherwise duplicate it (see `drop_redundant_leading_h2`/`REDUNDANT_LEADING_HEADINGS`). FAQ page also gets `FAQPage` JSON-LD auto-extracted from its own Q&A markup (`build_faq_schema`). Blog articles go through `ArticleRebuilder` (an HTMLParser subclass) that re-emits only whitelisted tags with guaranteed-balanced nesting — Shopify's raw markup has unbalanced divs that break layout if passed through — and get `BlogPosting` JSON-LD.
- `tools/gen_404.py` — generates `404.html` (`noindex`, crawlable). Needs a scratch-dir arg too, even though it uses no scraped data, because it imports `gen.py` which requires one at module load. Regenerate whenever header/footer change.
- `tools/gen_sitemap.py` — generates `sitemap.xml` from the same scraped product/collection data as `gen.py`, so it can never drift from the actual page set. Excludes `404.html` (correct — error pages don't belong in sitemaps).
- `assets/css/style.css` — single stylesheet for the whole site. Pages reference it with a cache-busting query (`style.css?v=N`); **bump N in `gen.py`'s `head()` and regenerate whenever the CSS changes**, or browsers serve stale styles.
- `assets/js/site.js` — all interactivity: mobile nav, hero slideshow, product gallery thumbs, contact/newsletter forms (they open WhatsApp with a prefilled message — no backend).

**After any generator run, regenerate everything together** (`gen.py`, `gen_pages.py`, `gen_404.py`, `gen_sitemap.py`, all with the same scratch-dir arg) — they share state (`SITE_URL`, product data) and a partial regen can leave pages out of sync.

## Conventions

- All internal links **must stay relative** (`../` style) — historically for GitHub Pages project-path portability; now less critical since the site lives at the custom domain root, but keep it anyway (still works everywhere, zero cost).
- SEO: every page has a unique meta description, self-referencing canonical, OG/Twitter tags, and appropriate JSON-LD (`Organization`+`WebSite` on home, `Product` on product pages, `BreadcrumbList` on collections, `FAQPage` on the FAQ, `BlogPosting` on posts) — all via `head()`'s `schema`/`description`/`canonical_path` params, never hand-added per page. `robots.txt` and `sitemap.xml` live at repo root; `sitemap.xml` is generated (see above), `robots.txt` is a static 4-line file (edit directly if it ever needs to change — no generator for something that small and static).
- Design system: brand pink `--pink: #e91e8c` / `--pink-dark: #c2185b`, announcement marquee salmon `#ee9599`, headings in Roboto Serif, body in Jost (both self-hosted in `assets/fonts/`, same families as the live store). WhatsApp green and Instagram gradient are reserved for their own CTAs.
- External links: `target="_blank" rel="noopener"`.
- `Archive-will-be-deleted/` is source photography/video only — never served, never modified, excluded from link checks.
- Commit policy (from `.claude/team/team-config.md`): agents never commit or push; the human does. Protected branch: `main`.

## Deploy

Workflow uploads the repo root as the Pages artifact (`enablement: true` self-enables Pages). `.nojekyll` present. If Pages enablement fails in CI, the one-time manual fallback is Settings → Pages → Source: GitHub Actions. Custom domain `littlepinkllama.com` is set via the `CNAME` file — if that file is ever missing, GitHub Pages falls back to serving the `github.io` URL and the domain stops resolving; don't delete it.
