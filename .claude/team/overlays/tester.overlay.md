# Overlay — tester — littlepinkllama

## Build / Test — exact commands
- Build command: none — no build step (plain static HTML/CSS/JS).
- Test command: `python -m http.server 8080` from repo root, then verify pages load (HTTP 200), no broken links/images, no console errors.

## Run for testing
- Local run: `python -m http.server 8080` (from repo root)
- Dev-server deploy (if used): NA
- Dev server address: http://localhost:8080/

## Environment prerequisites — check BEFORE any test execution
- Required connectivity/access: none beyond localhost; Node/npx on PATH required only for Playwright MCP browser cases.
- If any prerequisite is unmet: STOP and report to Jarvis — never emulate or mock around it.

## Health check
- URL: http://localhost:8080/
- Expected: HTTP 200 with homepage HTML (Little Pink Llama hero content present)

## UI scope
- UI location(s): all pages — home, collection pages (Shop All, Brooches, Hairclips, Crochet Toys, Collar, Rakhis), product pages, About, Contact, Blogs, FAQ, policy pages, sitemap.
- Rendering states to always check: mobile viewport (375px) and desktop (1440px); WhatsApp/Instagram CTA buttons present and correctly linked on every product page; floating WhatsApp button on all pages.

## Feature flags
- Mechanism & where to toggle: NA

## Adjacent-regression map
- Features most often broken by side effects: shared header/footer markup duplicated across pages (nav links drift), product data in `assets/js/products.js` vs static product pages (name/price mismatch), relative path breakage under GitHub Pages project path.

## Artifacts to collect
- Default evidence + capture method: page screenshots via Playwright MCP saved to `.claude/team/artifacts/<run>/`.

## Verify
1. Build: none — skip.
2. Start `python -m http.server 8080`; confirm the health check returns HTTP 200 with homepage HTML at http://localhost:8080/.
3. Verify pages load, no broken links/images, no console errors.
4. Execute the approved G2.7 test-case list plus the Regression scope; record results per team-protocol §2-artifacts.
