# Design — Little Pink Llama static replica

Date: 2026-08-13 · Status: implemented · Approved by owner ("complete all in 1 shot")

## Goal
Replicate littlepinkllama.com (owner's Shopify store) as a static site: same page count and design, **no sales/payment/cart** — every order CTA routes to WhatsApp (+91 94600 74404) or Instagram DM (@little_pink_llama_).

## Decisions
- **Stack:** plain HTML/CSS/JS, zero dependencies, no build step (owner choice).
- **Hosting:** GitHub Pages via Actions workflow; all links relative so project-path URLs work.
- **Products:** all shown available (no "Sold out"), prices visible, per-product WhatsApp deep link prefills product name + price.
- **Content:** scraped from the owner's live store (catalog via `/products.json`, pages/blogs via HTML). Payment references (Razorpay/COD in FAQ, Shopify in privacy policy) rewritten to the WhatsApp ordering flow.
- **Images:** downloaded from the store CDN at 900px (products) / 1600px (banners) into `assets/images/`; `Archive-will-be-deleted/` kept as unused source media.
- **Forms:** contact + newsletter open WhatsApp with prefilled message — no backend.

## Page inventory (74 files)
home (1) · collections (7) · products (53) · pages: about, contact, faq, shipping, return, terms, privacy, sitemap (8) · blogs: index + 3 posts (4) · 404 (1)

## Generators
`tools/gen.py` (home/collections/products) and `tools/gen_pages.py` (content pages) read scraped JSON/HTML from a scratch dir. One-time scaffold; output HTML is committed and hand-editable.

## Verification
- Link/asset checker: 73 pages, 0 broken internal refs, 0 leftover Shopify markup/cart references.
- Local serve smoke test: key pages HTTP 200, no mojibake.
