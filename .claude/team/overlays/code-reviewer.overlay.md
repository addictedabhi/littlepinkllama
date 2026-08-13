# Overlay — code-reviewer — littlepinkllama

## Code style
- Style references: match touched files; semantic HTML5, relative asset paths (GitHub Pages project-path safe), kebab-case filenames, no inline styles except dynamic values.

## Review checklist
- Project checklist (if any): NA — use the plugin's default review checklist. Project-specific musts: no payment/checkout/cart code anywhere; every order CTA points to WhatsApp `https://wa.me/919460074404` or Instagram `https://www.instagram.com/little_pink_llama_/`; all links/images relative; external links use `rel="noopener"`.

## Secret scanning
- Patterns/locations to scan: default common token/key/password patterns; site must contain zero secrets (no API keys — static site).

## Scope
- Out of review scope: `Archive-will-be-deleted/` (source media, will be deleted), `assets/images/` binary content (verify references only).
