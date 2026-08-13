# Overlay — technical-architect — littlepinkllama

All facts here are project-specific by design.

## Module map
- Source layout: static site at repo root — `index.html`; `pages/` (collections, products, about, contact, blogs, policies); `assets/css/`, `assets/js/` (incl. `products.js` product data), `assets/images/`; `Archive-will-be-deleted/` = source media only, never served.
- Key modules & owners: single-owner personal project (Abhishek Jain); modules = homepage, collection pages, product pages, content pages, shared header/footer, WhatsApp/Instagram CTA components.

## Data model & migrations
- Database(s): none — static site; product catalog lives in `assets/js/products.js` (JSON).
- Versioned-migration mechanism & location: NA

## API conventions
- Style/contract rules: NA — no backend. External integrations are link-outs only: WhatsApp deep links (`https://wa.me/919460074404?text=...`) and Instagram profile link.

## ADRs
- Location: docs/adr/
- Format: Nygard
- Current highest number: 0 (none yet)

## Security posture notes
- Auth mechanism: none — public static site, no login/cart/checkout by design.
- Known sensitive areas: no secrets permitted anywhere; external links need `rel="noopener"`; no payment functionality may ever be introduced without owner approval.

## Verify (for plan verification steps)
- Build: none — no build step.
- Test: `python -m http.server 8080` from repo root; pages return HTTP 200, no broken links/images, no console errors.
