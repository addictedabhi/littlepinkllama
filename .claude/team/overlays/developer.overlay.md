# Overlay — developer — littlepinkllama

## Repo & layout
- Repo root: (this repository). Main source: repo root — static site (`index.html`, `pages/`, `assets/css/`, `assets/js/`, `assets/images/`). `Archive-will-be-deleted/` is source media only — never modify, never serve from it directly; copy needed images into `assets/images/`.
- Test source: no automated test suite — verification is browser-based (see tester overlay).

## Toolchain
- Required toolchain: none for build (plain HTML/CSS/JS). Python 3 (already on machine) for local static server. Node/npx optional, only for Playwright MCP browser checks.
- If a required tool is missing on the machine: Python from python.org or `winget install Python.Python.3`; Node LTS via `winget install OpenJS.NodeJS.LTS`.
- Dependency policy: no package manifests — site must remain dependency-free (no CDN scripts requiring build steps); adding any external library requires explicit plan approval.

## Verify — exact commands
- Full build (never skip tests for verification): none — no build step; verification = serve and load pages without errors.
- Full test run: `python -m http.server 8080` from repo root, then verify pages load (HTTP 200), no broken links/images, no console errors.
- Affected-module test run (optional): NA

## Style & conventions
- Style reference: match touched files; semantic HTML, relative paths only (site must work under GitHub Pages project path `/littlepinkllama/`), kebab-case file names.
- Input-validation boundary layer: NA — static site, no server-side input handling; any client-side form input sanitized in JS before use.

## Branching & commits
- Feature branch naming: feature/<short-description> (lowercase, hyphen-separated)
- Protected branch (never commit directly): main
