# Little Pink Llama — Static Site

Static replica of [littlepinkllama.com](https://littlepinkllama.com/) (the owner's Shopify store) with **no payments, cart, or checkout**. Ordering happens via:

- **WhatsApp:** [+91 94600 74404](https://wa.me/919460074404)
- **Instagram DM:** [@little_pink_llama_](https://www.instagram.com/little_pink_llama_/)

## Structure

| Path | What |
|------|------|
| `index.html` | Homepage (hero slideshow, collections, latest, bulk orders, featured, testimonials, newsletter) |
| `collections/*.html` | Shop All, Brooches, Hairclips, Crochet toys, Collar, Rakhis, Featured (7 pages) |
| `products/*.html` | One page per product (53 pages) with gallery + WhatsApp/Instagram order buttons |
| `pages/*.html` | About, Contact, FAQ, Shipping/Return/Terms/Privacy policies, Sitemap |
| `blogs/*.html` | Blog index + 3 posts |
| `assets/` | CSS, JS, images (products + banners) |
| `tools/gen.py`, `tools/gen_pages.py` | One-time generators used to scaffold pages from scraped Shopify data |

## Run locally

```
python -m http.server 8080
```

Open http://localhost:8080/. No build step — plain HTML/CSS/JS, no dependencies.

## Deploy

Pushes to `main` deploy automatically to GitHub Pages via `.github/workflows/deploy.yml`.
One-time setup: repo **Settings → Pages → Source: GitHub Actions**.

All internal links are relative, so the site works at `https://<user>.github.io/littlepinkllama/` and on a custom domain.

## Notes

- `Archive-will-be-deleted/` holds original product photography/video sources — not served by the site.
- Contact + newsletter forms open WhatsApp with a prefilled message (no backend).
